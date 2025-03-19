from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, database
from .database import engine, get_db
from datetime import datetime, timedelta
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
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
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
            result[record.site_id] = {
                "url": site_url,
                "status": record.status,
                "last_updated": record.last_updated
            }
    
    # Add any missing sites with unknown status
    for site_id, url in MONITORED_SITES.items():
        if site_id not in result:
            result[site_id] = {
                "url": url,
                "status": "Unknown",
                "last_updated": None
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
        "site_id": site_id,
        "url": MONITORED_SITES.get(site_id, "Unknown"),
        "total_requests_24h": total_requests,
        "successful_requests_24h": successful_requests,
        "failed_requests_24h": failed_requests,
        "success_rate_24h": (successful_requests / total_requests) * 100 if total_requests > 0 else 0,
        "avg_response_time_24h": avg_response_time
    } 