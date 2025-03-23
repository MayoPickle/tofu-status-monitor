from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any, Type

class RequestMetricBase(BaseModel):
    site_id: str = "main"
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
    site_id: str = "main"
    endpoint: str
    average_time: float
    week_start: datetime
    week_end: datetime

class WeeklyAverage(WeeklyAverageBase):
    id: int

    class Config:
        orm_mode = True

class SiteStatusBase(BaseModel):
    site_id: str
    status: str
    
class SiteStatusCreate(SiteStatusBase):
    pass

class SiteStatus(SiteStatusBase):
    id: int
    last_updated: datetime
    
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
    site_permissions: Optional[Dict[str, List[str]]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

        @staticmethod
        def schema_extra(schema: Dict[str, Any], model: Type['UserResponse']) -> None:
            props = schema.get('properties', {})
            if 'site_permissions' in props:
                props['sitePermissions'] = props.pop('site_permissions')

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: str

class UptimeData(BaseModel):
    last_24h: float
    last_7d: float
    last_30d: float
    current_month: float

class HistoricalMetric(BaseModel):
    timestamp: datetime
    avg_response_time: float

class SitePermissionsUpdate(BaseModel):
    sitePermissions: Dict[str, List[str]] 