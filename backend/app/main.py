from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, database
from .database import engine, get_db
from datetime import datetime, timedelta
from typing import List
import jwt
from jwt.exceptions import PyJWTError

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