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

celery_app.conf.beat_schedule = {
    'monitor-kepler-endpoint': {
        'task': 'app.celery_worker.monitor_endpoint',
        'schedule': 60.0,  # Every 60 seconds
    },
    'calculate-weekly-average': {
        'task': 'app.celery_worker.calculate_weekly_average',
        'schedule': 3600.0,  # Every hour
    },
}

@celery_app.task
def monitor_endpoint():
    kepler_url = os.getenv("KEPLER_API_URL")
    db = database.SessionLocal()
    
    try:
        start_time = time.time()
        response = httpx.get(kepler_url, timeout=10.0)
        request_time = time.time() - start_time
        
        # Store the metrics in database
        db_metric = models.RequestMetric(
            endpoint=kepler_url,
            request_time=request_time,
            status_code=response.status_code
        )
        db.add(db_metric)
        db.commit()
        
        return {
            "status": "success",
            "endpoint": kepler_url,
            "request_time": request_time,
            "status_code": response.status_code
        }
    except Exception as e:
        # Store failed request
        db_metric = models.RequestMetric(
            endpoint=kepler_url,
            request_time=-1,  # Use -1 to indicate error
            status_code=0  # Use 0 to indicate error
        )
        db.add(db_metric)
        db.commit()
        
        return {
            "status": "error",
            "endpoint": kepler_url,
            "error": str(e)
        }
    finally:
        db.close()

@celery_app.task
def calculate_weekly_average():
    """Calculate weekly average request times and store in the database"""
    db = database.SessionLocal()
    kepler_url = os.getenv("KEPLER_API_URL")
    
    try:
        # Calculate date range for the last week
        now = datetime.now()
        week_ago = now - timedelta(days=7)
        
        # Query all successful requests from the last week
        metrics = db.query(models.RequestMetric).filter(
            models.RequestMetric.endpoint == kepler_url,
            models.RequestMetric.request_time > 0,  # Only successful requests
            models.RequestMetric.timestamp >= week_ago
        ).all()
        
        if metrics:
            # Calculate average
            avg_time = sum(metric.request_time for metric in metrics) / len(metrics)
            
            # Store weekly average
            db_avg = models.WeeklyAverage(
                endpoint=kepler_url,
                average_time=avg_time,
                week_start=week_ago,
                week_end=now
            )
            db.add(db_avg)
            db.commit()
            
            return {
                "status": "success",
                "average_time": avg_time,
                "sample_size": len(metrics)
            }
        else:
            return {
                "status": "error",
                "message": "No metrics found for the last week"
            }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
    finally:
        db.close() 