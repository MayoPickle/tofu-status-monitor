from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class RequestMetricBase(BaseModel):
    endpoint: str
    request_time: float
    status_code: int

class RequestMetricCreate(RequestMetricBase):
    pass

class RequestMetric(RequestMetricBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

class WeeklyAverageBase(BaseModel):
    endpoint: str
    average_time: float
    week_start: datetime
    week_end: datetime

class WeeklyAverage(WeeklyAverageBase):
    id: int

    class Config:
        orm_mode = True 