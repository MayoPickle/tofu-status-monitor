from datetime import datetime
from pydantic import BaseModel, EmailStr
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

class UserBase(BaseModel):
    username: str
    email: EmailStr
    name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    assigned_sites: Optional[List[str]] = None

class UserResponse(UserBase):
    id: int
    role: str
    assigned_sites: List[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: str 