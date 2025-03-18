from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, database
from .database import engine, get_db
from datetime import datetime, timedelta
from typing import List

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Kepler API", description="A monitoring application by Valtech")

# Add CORS middleware to allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Kepler API is running", "author": "Valtech"}

@app.get("/metrics/recent", response_model=List[schemas.RequestMetric])
def get_recent_metrics(limit: int = 100, db: Session = Depends(get_db)):
    """Get recent request metrics"""
    metrics = db.query(models.RequestMetric).order_by(
        models.RequestMetric.timestamp.desc()
    ).limit(limit).all()
    return metrics

@app.get("/metrics/averages", response_model=List[schemas.WeeklyAverage])
def get_weekly_averages(weeks: int = 4, db: Session = Depends(get_db)):
    """Get weekly average metrics"""
    averages = db.query(models.WeeklyAverage).order_by(
        models.WeeklyAverage.week_end.desc()
    ).limit(weeks).all()
    return averages

@app.get("/metrics/stats")
def get_stats(db: Session = Depends(get_db)):
    """Get statistics about the monitored endpoint"""
    # Get stats for the last 24 hours
    day_ago = datetime.now() - timedelta(days=1)
    
    # Total requests in the last 24 hours
    total_requests = db.query(models.RequestMetric).filter(
        models.RequestMetric.timestamp >= day_ago
    ).count()
    
    # Successful requests (status_code 200-299)
    successful_requests = db.query(models.RequestMetric).filter(
        models.RequestMetric.timestamp >= day_ago,
        models.RequestMetric.status_code >= 200,
        models.RequestMetric.status_code < 300
    ).count()
    
    # Failed requests
    failed_requests = total_requests - successful_requests
    
    # Average response time for successful requests
    avg_query = db.query(models.RequestMetric).filter(
        models.RequestMetric.timestamp >= day_ago,
        models.RequestMetric.request_time > 0
    ).all()
    
    avg_response_time = 0
    if avg_query:
        avg_response_time = sum(r.request_time for r in avg_query) / len(avg_query)
    
    return {
        "total_requests_24h": total_requests,
        "successful_requests_24h": successful_requests,
        "failed_requests_24h": failed_requests,
        "success_rate_24h": (successful_requests / total_requests) * 100 if total_requests > 0 else 0,
        "avg_response_time_24h": avg_response_time
    } 