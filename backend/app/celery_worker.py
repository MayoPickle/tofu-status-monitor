import os
import time
import httpx
from celery import Celery
from datetime import datetime, timedelta
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from . import models, database

load_dotenv()

# 创建logs目录如果不存在
logs_dir = Path(__file__).parent.parent / 'logs'
logs_dir.mkdir(exist_ok=True)

# 设置日志配置
celery_log_file = logs_dir / 'celery.log'
logger = logging.getLogger('celery')

# 设置日志轮换，最大10MB，保留5个备份
handler = RotatingFileHandler(
    str(celery_log_file),
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

celery_app = Celery(
    "kepler_monitor",
    broker=os.getenv("REDIS_URL"),
    backend=os.getenv("REDIS_URL")
)

celery_app.conf.update(
    worker_log_file=str(logs_dir / 'celery_worker.log'),
    beat_log_file=str(logs_dir / 'celery_beat.log'),
    task_log_file=str(logs_dir / 'celery_tasks.log'),
)

# 日志轮换配置
celery_app.conf.worker_log_size = 10 * 1024 * 1024  # 10MB
celery_app.conf.worker_log_backups = 5
celery_app.conf.beat_log_size = 10 * 1024 * 1024  # 10MB
celery_app.conf.beat_log_backups = 5

# 定义监控的URLs
MONITORED_SITES = {
    'main': os.getenv("KEPLER_API_URL"),
    'backup': os.getenv("BACKUP_API_URL"),
    'staging': os.getenv("STAGING_API_URL")
}

celery_app.conf.beat_schedule = {
    'monitor-main-endpoint': {
        'task': 'app.celery_worker.monitor_site',
        'schedule': 60.0,  # Every 60 seconds
        'args': ('main',)
    },
    'monitor-backup-endpoint': {
        'task': 'app.celery_worker.monitor_site',
        'schedule': 60.0,  # Every 60 seconds
        'args': ('backup',)
    },
    'monitor-staging-endpoint': {
        'task': 'app.celery_worker.monitor_site',
        'schedule': 60.0,  # Every 60 seconds
        'args': ('staging',)
    },
    'calculate-weekly-average': {
        'task': 'app.celery_worker.calculate_weekly_average',
        'schedule': 3600.0,  # Every hour
    },
    'update-site-statuses': {
        'task': 'app.celery_worker.update_site_statuses',
        'schedule': 300.0,  # Every 5 minutes
    },
}

@celery_app.task
def monitor_site(site_id):
    """Monitor a specific site identified by site_id"""
    if site_id not in MONITORED_SITES:
        logger.error(f"Unknown site_id: {site_id}")
        return {"status": "error", "message": f"Unknown site_id: {site_id}"}
    
    url = MONITORED_SITES[site_id]
    if not url:
        logger.error(f"No URL configured for site: {site_id}")
        return {"status": "error", "message": f"No URL configured for site: {site_id}"}
    
    db = database.SessionLocal()
    
    try:
        start_time = time.time()
        response = httpx.get(url, timeout=10.0)
        request_time = time.time() - start_time
        
        # Store the metrics in database
        db_metric = models.RequestMetric(
            site_id=site_id,
            endpoint=url,
            request_time=request_time,
            status_code=response.status_code
        )
        db.add(db_metric)
        db.commit()
        
        logger.info(f"Monitored {site_id} ({url}): {response.status_code} in {request_time:.2f}s")
        
        return {
            "status": "success",
            "site_id": site_id,
            "endpoint": url,
            "request_time": request_time,
            "status_code": response.status_code
        }
    except Exception as e:
        # Store failed request
        db_metric = models.RequestMetric(
            site_id=site_id,
            endpoint=url,
            request_time=-1,  # Use -1 to indicate error
            status_code=0  # Use 0 to indicate error
        )
        db.add(db_metric)
        db.commit()
        
        logger.error(f"Error monitoring {site_id} ({url}): {str(e)}")
        
        return {
            "status": "error",
            "site_id": site_id,
            "endpoint": url,
            "error": str(e)
        }
    finally:
        db.close()

@celery_app.task
def update_site_statuses():
    """Update the status of all monitored sites"""
    db = database.SessionLocal()
    
    try:
        results = {}
        
        # For each site, determine status based on recent metrics
        for site_id, url in MONITORED_SITES.items():
            # Get the most recent 5 metrics
            recent_metrics = db.query(models.RequestMetric).filter(
                models.RequestMetric.site_id == site_id
            ).order_by(
                models.RequestMetric.timestamp.desc()
            ).limit(5).all()
            
            # Determine status
            status = "Unknown"
            if recent_metrics:
                # Count successful requests (status code 200-299)
                success_count = sum(1 for m in recent_metrics if 200 <= m.status_code < 300)
                
                # If more than 60% are successful, status is "Good"
                if success_count / len(recent_metrics) >= 0.6:
                    status = "Good"
                else:
                    status = "Bad"
            
            # Update or create status record
            status_record = db.query(models.SiteStatus).filter(
                models.SiteStatus.site_id == site_id
            ).first()
            
            if status_record:
                status_record.status = status
                status_record.last_updated = datetime.now()
            else:
                status_record = models.SiteStatus(
                    site_id=site_id,
                    status=status
                )
                db.add(status_record)
            
            results[site_id] = {
                "url": url,
                "status": status
            }
        
        db.commit()
        logger.info(f"Updated site statuses: {results}")
        return results
    except Exception as e:
        logger.error(f"Error updating site statuses: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }
    finally:
        db.close()

@celery_app.task
def calculate_weekly_average():
    """Calculate weekly average request times and store in the database"""
    db = database.SessionLocal()
    
    try:
        # Calculate date range for the last week
        now = datetime.now()
        week_ago = now - timedelta(days=7)
        
        results = {}
        
        # Calculate for each site
        for site_id, url in MONITORED_SITES.items():
            # Query all successful requests from the last week
            metrics = db.query(models.RequestMetric).filter(
                models.RequestMetric.site_id == site_id,
                models.RequestMetric.request_time > 0,  # Only successful requests
                models.RequestMetric.timestamp >= week_ago
            ).all()
            
            if metrics:
                # Calculate average
                avg_time = sum(metric.request_time for metric in metrics) / len(metrics)
                
                # Store weekly average
                db_avg = models.WeeklyAverage(
                    site_id=site_id,
                    endpoint=url,
                    average_time=avg_time,
                    week_start=week_ago,
                    week_end=now
                )
                db.add(db_avg)
                
                results[site_id] = {
                    "status": "success",
                    "average_time": avg_time,
                    "sample_size": len(metrics)
                }
            else:
                results[site_id] = {
                    "status": "error",
                    "message": f"No metrics found for {site_id} in the last week"
                }
        
        db.commit()
        return results
    except Exception as e:
        logger.error(f"Error calculating weekly averages: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }
    finally:
        db.close() 