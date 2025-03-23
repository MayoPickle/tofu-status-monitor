# Kepler

A monitoring application by Valtech that tracks the performance of the `https://yudoufu.org/tofu/rooms/` endpoint. The application collects metrics every 60 seconds, calculates weekly averages, and visualizes the results through a web interface.

## Technologies Used

- **Backend**:
  - FastAPI: Modern, high-performance web framework for building APIs
  - Celery: Distributed task queue for scheduling periodic checks
  - PostgreSQL: Database for storing performance metrics
  - Redis: Message broker for Celery tasks
  - SQLAlchemy: SQL toolkit and ORM
  - Alembic: Database migration tool

- **Frontend**:
  - Vue.js 3: Progressive JavaScript framework
  - Chart.js: JavaScript charting library for data visualization
  - Axios: Promise-based HTTP client

## Project Structure

```
kepler/
├── backend/              # FastAPI backend application
│   ├── app/              # Application code
│   │   ├── models.py     # Database models
│   │   ├── schemas.py    # Pydantic schemas
│   │   ├── main.py       # FastAPI application
│   │   └── celery_worker.py # Celery tasks and configuration
│   ├── migrations/       # Alembic database migrations
│   ├── requirements.txt  # Python dependencies
│   ├── .env              # Environment variables
│   └── run.sh            # Script to run the backend
├── frontend/             # Vue.js frontend application
│   ├── src/              # Source code
│   │   ├── components/   # Vue components
│   │   ├── views/        # Vue views
│   │   ├── router/       # Vue Router configuration
│   │   ├── App.vue       # Main Vue component
│   │   └── main.js       # Vue application entry point
│   └── package.json      # Node.js dependencies
└── README.md             # Project documentation
```

## Setup and Installation

### Prerequisites

- Python 3.8+
- Node.js 14+
- PostgreSQL
- Redis

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Update the `.env` file with your database and Redis connection details (already configured for this deployment).

4. Initialize the database:
   ```
   alembic upgrade head
   ```

5. Run the application:
   ```
   ./run.sh
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Run the development server:
   ```
   npm run serve
   ```

4. Build for production:
   ```
   npm run build
   ```

## Features

- **Real-time Monitoring**: Checks endpoint every 60 seconds
- **Performance Metrics**: Tracks response time and status codes
- **Weekly Averages**: Calculates and stores average response times on a weekly basis
- **Dashboard**: Visual overview of current status and recent performance
- **Detailed Metrics**: In-depth analysis of collected data 