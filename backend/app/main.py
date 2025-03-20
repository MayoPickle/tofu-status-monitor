from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, database
from .database import engine, get_db
from datetime import UTC, datetime, timedelta
from typing import List, Dict
import jwt
from jwt.exceptions import PyJWTError
import os

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

# Monitored sites
MONITORED_SITES = {
    'main': os.getenv("KEPLER_API_URL", "https://yudoufu.org/"),
    'backup': os.getenv("BACKUP_API_URL", "https://github.com"),
    'staging': os.getenv("STAGING_API_URL", "https://google.com")
}

# JWT Configuration
SECRET_KEY = "your-secret-key"  # In production, use a secure secret key from environment variables
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Helper functions
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except PyJWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

def get_admin_user(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

# Auth endpoints
@app.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if username exists
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email exists
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = models.User.hash_password(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        name=user.name,
        hashed_password=hashed_password,
        role="user",  # Default role for new registrations
        assigned_sites=[]  # Empty list for new users
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@app.get("/users", response_model=List[schemas.UserResponse])
def get_all_users(current_user: models.User = Depends(get_admin_user), db: Session = Depends(get_db)):
    """Get all users - admin only endpoint"""
    users = db.query(models.User).all()
    return users

@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: int, 
    user_update: schemas.UserUpdate, 
    current_user: models.User = Depends(get_admin_user), 
    db: Session = Depends(get_db)
):
    """Update a user - admin only endpoint"""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user fields
    update_data = user_update.dict(exclude_unset=True)
    
    # If password is provided, hash it
    if "password" in update_data and update_data["password"]:
        update_data["hashed_password"] = models.User.hash_password(update_data.pop("password"))
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int, 
    current_user: models.User = Depends(get_admin_user), 
    db: Session = Depends(get_db)
):
    """Delete a user - admin only endpoint"""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prevent self-deletion
    if db_user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    
    db.delete(db_user)
    db.commit()
    return None

@app.put("/users/{user_id}/permissions", response_model=schemas.UserResponse)
def update_user_permissions(
    user_id: int, 
    permissions: schemas.SitePermissionsUpdate, 
    current_user: models.User = Depends(get_admin_user), 
    db: Session = Depends(get_db)
):
    """Update a user's site permissions - admin only endpoint"""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update the site_permissions field
    db_user.site_permissions = permissions.sitePermissions
    
    # For backward compatibility, also update the assigned_sites field
    db_user.assigned_sites = list(permissions.sitePermissions.keys())
    
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/admin/migrate-user-permissions", status_code=200)
def migrate_user_permissions(
    current_user: models.User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Migrate all users' assigned_sites to the new site_permissions format - admin only endpoint"""
    users = db.query(models.User).all()
    updated_count = 0
    
    # Default permissions based on role
    default_permissions = {
        "admin": ["site_view", "site_view_metrics", "site_configure", "site_add", "site_edit", "site_delete"],
        "maintainer": ["site_view", "site_view_metrics", "site_configure", "site_edit"],
        "user": ["site_view", "site_view_metrics"],
        "guest": ["site_view"]
    }
    
    for user in users:
        # Skip users who already have site_permissions
        if user.site_permissions:
            continue
            
        # Create site_permissions from assigned_sites
        site_permissions = {}
        for site_id in user.assigned_sites:
            # Assign default permissions based on user role
            role = user.role.lower()
            permissions = default_permissions.get(role, ["site_view"])
            site_permissions[site_id] = permissions
        
        # Update user
        user.site_permissions = site_permissions
        updated_count += 1
    
    db.commit()
    return {"message": f"Successfully migrated {updated_count} users' permissions"}

@app.get("/")
def read_root():
    return {"status": "Kepler API is running", "author": "Valtech"}

@app.get("/metrics/recent", response_model=List[schemas.RequestMetric])
def get_recent_metrics(limit: int = 100, site_id: str = "main", db: Session = Depends(get_db)):
    """Get recent request metrics"""
    metrics = db.query(models.RequestMetric).filter(
        models.RequestMetric.site_id == site_id
    ).order_by(
        models.RequestMetric.timestamp.desc()
    ).limit(limit).all()
    return metrics

@app.get("/metrics/averages", response_model=List[schemas.WeeklyAverage])
def get_weekly_averages(weeks: int = 4, site_id: str = "main", db: Session = Depends(get_db)):
    """Get weekly average metrics"""
    averages = db.query(models.WeeklyAverage).filter(
        models.WeeklyAverage.site_id == site_id
    ).order_by(
        models.WeeklyAverage.week_end.desc()
    ).limit(weeks).all()
    return averages

@app.get("/metrics/status")
def get_status(db: Session = Depends(get_db)):
    """Get current status of all monitored sites"""
    status_records = db.query(models.SiteStatus).all()
    result = {}
    
    # Create a dict of statuses
    for record in status_records:
        site_url = MONITORED_SITES.get(record.site_id)
        if site_url:
            # Get the most recent metric to get the HTTP status code
            latest_metric = db.query(models.RequestMetric).filter(
                models.RequestMetric.site_id == record.site_id
            ).order_by(models.RequestMetric.timestamp.desc()).first()
            
            http_status = None
            if latest_metric and latest_metric.status_code > 0:
                http_status = latest_metric.status_code
            
            result[record.site_id] = {
                "url": site_url,
                "status": record.status,
                "last_updated": record.last_updated,
                "http_status": http_status
            }
    
    # Add any missing sites with unknown status
    for site_id, url in MONITORED_SITES.items():
        if site_id not in result:
            result[site_id] = {
                "url": url,
                "status": "Unknown",
                "last_updated": None,
                "http_status": None
            }
            
    return result

@app.get("/sites", tags=["sites"])
def get_monitored_sites():
    """Get all monitored sites information"""
    result = []
    for site_id, url in MONITORED_SITES.items():
        result.append({
            "id": site_id,
            "name": site_id.capitalize(),
            "url": url
        })
    return result

@app.get("/metrics/stats")
def get_stats(site_id: str = "main", db: Session = Depends(get_db)):
    """Get statistics about the monitored endpoint"""
    # Get stats for the last 24 hours
    day_ago = datetime.now() - timedelta(days=1)
    
    # Total requests in the last 24 hours
    total_requests = db.query(models.RequestMetric).filter(
        models.RequestMetric.site_id == site_id,
        models.RequestMetric.timestamp >= day_ago
    ).count()
    
    # Successful requests (status_code 200-299)
    successful_requests = db.query(models.RequestMetric).filter(
        models.RequestMetric.site_id == site_id,
        models.RequestMetric.timestamp >= day_ago,
        models.RequestMetric.status_code >= 200,
        models.RequestMetric.status_code < 300
    ).count()
    
    # Failed requests
    failed_requests = total_requests - successful_requests
    
    # Average response time for successful requests
    avg_query = db.query(models.RequestMetric).filter(
        models.RequestMetric.site_id == site_id,
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

@app.get("/metrics/uptime", response_model=schemas.UptimeData)
def get_uptime(site_id: str = "main", db: Session = Depends(get_db)):
    """Calculate uptime based on successful requests"""
    # Last 24 hours
    day_ago = datetime.now() - timedelta(days=1)
    uptime_24h = calculate_uptime_for_period(db, site_id, day_ago, datetime.now())
    
    # Last 7 days
    week_ago = datetime.now() - timedelta(days=7)
    uptime_7d = calculate_uptime_for_period(db, site_id, week_ago, datetime.now())
    
    # Last 30 days
    month_ago = datetime.now() - timedelta(days=30)
    uptime_30d = calculate_uptime_for_period(db, site_id, month_ago, datetime.now())
    
    # Current month
    today = datetime.now()
    first_day_of_month = datetime(today.year, today.month, 1)
    uptime_current_month = calculate_uptime_for_period(db, site_id, first_day_of_month, today)
    
    return {
        "last_24h": uptime_24h,
        "last_7d": uptime_7d,
        "last_30d": uptime_30d,
        "current_month": uptime_current_month
    }

def calculate_uptime_for_period(db: Session, site_id: str, start_time: datetime, end_time: datetime):
    """Helper function to calculate uptime percentage for a given period"""
    # Get all metrics for the period
    metrics = db.query(models.RequestMetric).filter(
        models.RequestMetric.site_id == site_id,
        models.RequestMetric.timestamp >= start_time,
        models.RequestMetric.timestamp <= end_time
    ).all()
    
    if not metrics:
        return 100.0  # No metrics recorded = 100% uptime (or could return 0 or None)
    
    # Count successful requests (status code 200-299)
    successful = sum(1 for m in metrics if 200 <= m.status_code < 300)
    
    # Calculate uptime percentage
    return round((successful / len(metrics)) * 100.0, 2)

@app.get("/metrics/historical", response_model=List[schemas.HistoricalMetric])
def get_historical_metrics(period: str = "7d", site_id: str = "main", db: Session = Depends(get_db)):
    """Get historical metrics data for charts
    
    Periods supported:
    - 7d: Last 7 days (daily average)
    - 30d: Last 30 days (daily average)
    """
    today = datetime.now()
    
    if period == "7d":
        # Get data for the last 7 days
        start_date = today - timedelta(days=7)
        result = []
        
        # Calculate daily averages
        for i in range(7):
            day_start = start_date + timedelta(days=i)
            day_end = day_start + timedelta(days=1)
            
            # Get metrics for the day
            day_metrics = db.query(models.RequestMetric).filter(
                models.RequestMetric.site_id == site_id,
                models.RequestMetric.timestamp >= day_start,
                models.RequestMetric.timestamp < day_end
            ).all()
            
            # Calculate average response time
            avg_time = 0
            if day_metrics:
                avg_time = sum(m.request_time for m in day_metrics) / len(day_metrics)
            
            # Add data point
            result.append({
                "timestamp": day_start,
                "avg_response_time": avg_time
            })
        
        return result
    
    elif period == "30d":
        # Get data for the last 30 days
        start_date = today - timedelta(days=30)
        result = []
        
        # Calculate daily averages
        for i in range(30):
            day_start = start_date + timedelta(days=i)
            day_end = day_start + timedelta(days=1)
            
            # Get metrics for the day
            day_metrics = db.query(models.RequestMetric).filter(
                models.RequestMetric.site_id == site_id,
                models.RequestMetric.timestamp >= day_start,
                models.RequestMetric.timestamp < day_end
            ).all()
            
            # Calculate average response time
            avg_time = 0
            if day_metrics:
                avg_time = sum(m.request_time for m in day_metrics) / len(day_metrics)
            
            # Add data point
            result.append({
                "timestamp": day_start,
                "avg_response_time": avg_time
            })
        
        return result
    
    # Default case - return empty list
    return []

@app.post("/metrics/record", status_code=201)
def record_metric(metric: schemas.RequestMetricCreate, db: Session = Depends(get_db)):
    # Create new metric
    db_metric = models.RequestMetric(
        site_id=metric.site_id,
        status_code=metric.status_code,
        request_time=metric.request_time,
        timestamp=metric.timestamp
    )
    
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric 