from sqlalchemy import Column, Integer, Float, DateTime, String
from sqlalchemy.sql import func
from .database import Base

class RequestMetric(Base):
    __tablename__ = "request_metrics"

    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String, index=True)
    request_time = Column(Float)  # request duration in seconds
    status_code = Column(Integer)
    timestamp = Column(DateTime, default=func.now())

class WeeklyAverage(Base):
    __tablename__ = "weekly_averages"

    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String, index=True)
    average_time = Column(Float)
    week_start = Column(DateTime, index=True)
    week_end = Column(DateTime) 