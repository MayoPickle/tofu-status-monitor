<template>
  <div class="about">
    <div class="about-header">
      <h1>About Kepler</h1>
      <p class="subtitle">Elegant monitoring for your critical endpoints</p>
    </div>
    
    <div class="card-grid">
      <div class="card feature-card">
        <div class="card-icon">
          <svg viewBox="0 0 24 24">
            <path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4M12,6A6,6 0 0,0 6,12A6,6 0 0,0 12,18A6,6 0 0,0 18,12A6,6 0 0,0 12,6M12,8A4,4 0 0,1 16,12A4,4 0 0,1 12,16A4,4 0 0,1 8,12A4,4 0 0,1 12,8M12,9.8A2.2,2.2 0 0,0 9.8,12A2.2,2.2 0 0,0 12,14.2A2.2,2.2 0 0,0 14.2,12A2.2,2.2 0 0,0 12,9.8Z" />
          </svg>
        </div>
        <h2>Project Overview</h2>
        <p>
          Kepler is a status monitoring application designed by Valtech to track the performance and availability
          of the <code>https://yudoufu.org/tofu/rooms/</code> endpoint. The system performs regular checks every 
          60 seconds to ensure the endpoint is running properly and collects performance metrics.
        </p>
      </div>
      
      <div class="card tech-card">
        <div class="card-icon">
          <svg viewBox="0 0 24 24">
            <path d="M21,16.5C21,16.88 20.79,17.21 20.47,17.38L12.57,21.82C12.41,21.94 12.21,22 12,22C11.79,22 11.59,21.94 11.43,21.82L3.53,17.38C3.21,17.21 3,16.88 3,16.5V7.5C3,7.12 3.21,6.79 3.53,6.62L11.43,2.18C11.59,2.06 11.79,2 12,2C12.21,2 12.41,2.06 12.57,2.18L20.47,6.62C20.79,6.79 21,7.12 21,7.5V16.5M12,4.15L6.04,7.5L12,10.85L17.96,7.5L12,4.15M5,15.91L11,19.29V12.58L5,9.21V15.91M19,15.91V9.21L13,12.58V19.29L19,15.91Z" />
          </svg>
        </div>
        <h2>Technologies Used</h2>
        <div class="tech-grid">
          <div class="tech-item">
            <h3>Backend</h3>
            <ul>
              <li>FastAPI</li>
              <li>Celery</li>
              <li>PostgreSQL</li>
              <li>Redis</li>
            </ul>
          </div>
          <div class="tech-item">
            <h3>Frontend</h3>
            <ul>
              <li>Vue.js 3</li>
              <li>Chart.js</li>
              <li>Axios</li>
            </ul>
          </div>
        </div>
        <p>
          The backend uses Celery to schedule regular monitoring tasks with Redis as the message broker.
          All metrics are stored in PostgreSQL for long-term analysis. The frontend provides visualizations
          and real-time updates of the collected data.
        </p>
      </div>
      
      <div class="card metrics-card">
        <div class="card-icon">
          <svg viewBox="0 0 24 24">
            <path d="M19,3H5C3.89,3 3,3.89 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5C21,3.89 20.1,3 19,3M9,17H7V10H9V17M13,17H11V7H13V17M17,17H15V13H17V17Z" />
          </svg>
        </div>
        <h2>Metrics Collected</h2>
        <div class="metrics-list">
          <div class="metric-item">
            <div class="metric-bullet"></div>
            <div>
              <h3>Request Duration</h3>
              <p>Time taken to complete each request</p>
            </div>
          </div>
          <div class="metric-item">
            <div class="metric-bullet"></div>
            <div>
              <h3>Status Codes</h3>
              <p>HTTP status codes returned by the endpoint</p>
            </div>
          </div>
          <div class="metric-item">
            <div class="metric-bullet"></div>
            <div>
              <h3>Weekly Averages</h3>
              <p>Average response time calculated on a weekly basis</p>
            </div>
          </div>
          <div class="metric-item">
            <div class="metric-bullet"></div>
            <div>
              <h3>Success Rate</h3>
              <p>Percentage of successful requests</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="architecture-section">
      <div class="card architecture-card">
        <div class="card-icon">
          <svg viewBox="0 0 24 24">
            <path d="M3,3H21V21H3V3M7,7V9H9V15H7V17H13V15H11V9H13V7H7Z" />
          </svg>
        </div>
        <h2>System Architecture</h2>
        <div class="architecture-diagram">
          <pre class="diagram-text">
╔═════════════════════════════════╗
║         Client Browser          ║
╚═══════════════╦═════════════════╝
                ▼
╔═════════════════════════════════╗
║        Frontend (Vue.js)        ║
║  ┌───────────┐  ┌───────────┐   ║
║  │   Views   │  │Components │   ║
║  └─────┬─────┘  └─────┬─────┘   ║
║        └────────┬─────┘         ║
║         Vue Router/Store        ║
╚═══════════════╦═════════════════╝
      HTTP/REST ▼
╔═════════════════════════════════╗
║       Backend (FastAPI)         ║
║  ┌───────────┐  ┌───────────┐   ║
║  │   API     │  │   Auth    │   ║
║  │ Endpoints │  │  Service  │   ║
║  └─────┬─────┘  └─────┬─────┘   ║
║        └────────┬─────┘         ║
║         Database Models         ║
║         SQLAlchemy ORM          ║
╚═══════════════╦═════════════════╝
                ▼
╔═════════════════════════════════╗
║      PostgreSQL Database        ║
╚═══════════════╦═════════════════╝
                ▼
╔═════════════════════════════════╗
║        Celery Workers           ║
║  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓   ║
║  ┃  • Site Monitoring        ┃   ║
║  ┃  • Metrics Collection     ┃   ║
║  ┃  • Data Aggregation       ┃   ║
║  ┃  • Status Updates         ┃   ║
║  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛   ║
╚═══════════════╦═════════════════╝
                ▼
╔═════════════════════════════════╗
║      Redis (Task Queue)         ║
╚═══════════════╦═════════════════╝
                ▼
╔═════════════════════════════════╗
║     Celery Beat (Scheduling)    ║
╚═══════════════╦═════════════════╝
                ▼
╔═════════════════════════════════╗
║         Monitored Sites         ║
║                                 ║
║    Main     Backup    Staging   ║
╚═════════════════════════════════╝</pre>
        </div>
        <p>The Kepler monitoring system follows a modern architecture with a Vue.js frontend, FastAPI backend, and a robust worker system for continuous monitoring.</p>
      </div>
    </div>
    
    <div class="about-footer">
      <p>Built with <span class="heart">❤</span> by Valtech</p>
      <div class="version">Version 1.0.0</div>
    </div>
  </div>
</template>

<style scoped>
.about {
  max-width: 100%;
  padding-bottom: 2rem;
}

.about-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.about-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 1.25rem;
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
}

.architecture-section {
  margin-top: 2rem;
  width: 100%;
}

.card {
  background: var(--bg-secondary);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 2rem;
  position: relative;
  transition: var(--transition);
  height: 100%;
  display: flex;
  flex-direction: column;
  border: 1px solid var(--border-color);
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.card-icon {
  width: 48px;
  height: 48px;
  margin-bottom: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
}

.card-icon svg {
  width: 36px;
  height: 36px;
}

.feature-card .card-icon {
  background-color: rgba(42, 157, 143, 0.1);
}

.feature-card .card-icon svg {
  fill: var(--primary);
}

.architecture-card .card-icon {
  background-color: rgba(87, 115, 153, 0.1);
}

.architecture-card .card-icon svg {
  fill: #577399; /* Custom blue for architecture icon */
}

.architecture-card {
  background-color: var(--bg-secondary);
  width: 100%;
  margin-top: 2rem;
  grid-column: 1 / -1;
  padding: 2.5rem;
}

.architecture-card h2 {
  text-align: center;
  font-size: 1.75rem;
  margin-bottom: 1.5rem;
}

.architecture-diagram {
  width: 100%;
  overflow-x: auto;
  margin-bottom: 1.5rem;
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  background-color: var(--bg-primary);
  padding: 0.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.diagram-text {
  font-family: 'Menlo', 'Monaco', 'Consolas', monospace;
  font-size: 0.95rem;
  line-height: 1.4;
  color: var(--text-primary);
  padding: 1.5rem;
  margin: 0;
  white-space: pre;
}

/* Additional explanation text */
.architecture-card p {
  text-align: center;
  font-size: 1.1rem;
  max-width: 800px;
  margin: 1rem auto 0;
}

.tech-card .card-icon {
  background-color: rgba(233, 196, 106, 0.1);
}

.tech-card .card-icon svg {
  fill: var(--secondary);
}

.metrics-card .card-icon {
  background-color: rgba(244, 162, 97, 0.1);
}

.metrics-card .card-icon svg {
  fill: var(--accent);
}

.card h2 {
  margin-top: 0;
  margin-bottom: 1.25rem;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
}

.card p {
  font-size: 1rem;
  line-height: 1.6;
  color: var(--text-secondary);
  margin-bottom: 0;
}

code {
  background-color: var(--bg-primary);
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-family: 'Menlo', 'Monaco', 'Consolas', monospace;
  font-size: 0.9em;
  color: var(--primary);
}

.tech-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.tech-item h3 {
  font-size: 1.1rem;
  margin-top: 0;
  margin-bottom: 0.75rem;
  color: var(--text-primary);
  font-weight: 600;
}

.tech-item ul {
  padding-left: 1.25rem;
  margin: 0;
}

.tech-item li {
  margin-bottom: 0.5rem;
  color: var(--text-secondary);
}

.metrics-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.metric-item {
  display: flex;
  align-items: flex-start;
}

.metric-bullet {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: var(--primary);
  margin-top: 0.5rem;
  margin-right: 1rem;
  flex-shrink: 0;
}

.metric-item:nth-child(2) .metric-bullet {
  background-color: var(--secondary);
}

.metric-item:nth-child(3) .metric-bullet {
  background-color: var(--accent);
}

.metric-item:nth-child(4) .metric-bullet {
  background-color: var(--success);
}

.metric-item h3 {
  font-size: 1.1rem;
  margin: 0 0 0.25rem 0;
  color: var(--text-primary);
  font-weight: 600;
}

.metric-item p {
  margin: 0;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.about-footer {
  margin-top: 3rem;
  text-align: center;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.heart {
  color: #e74c3c;
  font-size: 1.1rem;
}

.version {
  margin-top: 0.5rem;
  opacity: 0.7;
}

@media (max-width: 768px) {
  .card-grid {
    grid-template-columns: 1fr;
  }
  
  .tech-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .about-header h1 {
    font-size: 2rem;
  }
  
  .subtitle {
    font-size: 1.1rem;
  }
  
  .architecture-card {
    order: unset;
    width: 100%;
  }
  
  .diagram-text {
    font-size: 0.75rem;
  }
}
</style> 