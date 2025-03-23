from sqlalchemy import Column, Integer, Float, DateTime, String, ARRAY
from sqlalchemy.sql import func
from .database import Base
import bcrypt
from sqlalchemy.dialects.postgresql import JSONB

class RequestMetric(Base):
    __tablename__ = "request_metrics"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(String, index=True, default="main")  # 'main', 'backup', 'staging'
    endpoint = Column(String, index=True)
    request_time = Column(Float)  # request duration in seconds
    status_code = Column(Integer)
    timestamp = Column(DateTime, default=func.now())

class WeeklyAverage(Base):
    __tablename__ = "weekly_averages"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(String, index=True, default="main")  # 'main', 'backup', 'staging'
    endpoint = Column(String, index=True)
    average_time = Column(Float)
    week_start = Column(DateTime, index=True)
    week_end = Column(DateTime)

# Status cache for site status
class SiteStatus(Base):
    __tablename__ = "site_statuses"
    
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(String, index=True, unique=True)
    status = Column(String)  # "Good", "Bad"
    last_updated = Column(DateTime, default=func.now(), onupdate=func.now())

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    role = Column(String, default="user")  # admin, maintainer, user, guest
    assigned_sites = Column(ARRAY(String), default=[])
    site_permissions = Column(JSONB, default={})  # New field for storing site permissions
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8')) 