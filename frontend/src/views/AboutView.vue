<template>
  <div class="about">
    <!-- 太空背景元素 -->
    <div class="stars">
      <div class="star" v-for="n in 80" :key="n" :style="{ 
        top: Math.random() * 100 + '%', 
        left: Math.random() * 100 + '%',
        width: (Math.random() * 2 + 1) + 'px',
        height: (Math.random() * 2 + 1) + 'px',
        animationDelay: Math.random() * 5 + 's'
      }"></div>
    </div>
    <div class="grid-lines"></div>
    <div class="planet-effect"></div>
    <div class="planet-ring"></div>
    <div class="orbital-path"></div>
    
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
<span class="diagram-highlight">╔═════════════════════════════════╗</span>
║         Client Browser          ║
<span class="diagram-highlight">╚═══════════════╦═════════════════╝</span>
                <span class="diagram-highlight">▼</span>
<span class="diagram-highlight">╔═════════════════════════════════╗</span>
║        Frontend (Vue.js)        ║
║  <span class="diagram-highlight">┌───────────┐</span>  <span class="diagram-highlight">┌───────────┐</span>   ║
║  │   Views   │  │Components │   ║
║  <span class="diagram-highlight">└─────┬─────┘</span>  <span class="diagram-highlight">└─────┬─────┘</span>   ║
║        <span class="diagram-highlight">└────────┬─────┘</span>         ║
║         Vue Router/Store        ║
<span class="diagram-highlight">╚═══════════════╦═════════════════╝</span>
      HTTP/REST <span class="diagram-highlight">▼</span>
<span class="diagram-highlight">╔═════════════════════════════════╗</span>
║       Backend (FastAPI)         ║
║  <span class="diagram-highlight">┌───────────┐</span>  <span class="diagram-highlight">┌───────────┐</span>   ║
║  │   API     │  │   Auth    │   ║
║  │ Endpoints │  │  Service  │   ║
║  <span class="diagram-highlight">└─────┬─────┘</span>  <span class="diagram-highlight">└─────┬─────┘</span>   ║
║        <span class="diagram-highlight">└────────┬─────┘</span>         ║
║         Database Models         ║
║         SQLAlchemy ORM          ║
<span class="diagram-highlight">╚═══════════════╦═════════════════╝</span>
                <span class="diagram-highlight">▼</span>
<span class="diagram-highlight">╔═════════════════════════════════╗</span>
║      PostgreSQL Database        ║
<span class="diagram-highlight">╚═══════════════╦═════════════════╝</span>
                <span class="diagram-highlight">▼</span>
<span class="diagram-highlight">╔═════════════════════════════════╗</span>
║        Celery Workers           ║
║  <span class="diagram-highlight">┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓</span>   ║
║  <span class="diagram-highlight">┃</span>  • Site Monitoring        <span class="diagram-highlight">┃</span>   ║
║  <span class="diagram-highlight">┃</span>  • Metrics Collection     <span class="diagram-highlight">┃</span>   ║
║  <span class="diagram-highlight">┃</span>  • Data Aggregation       <span class="diagram-highlight">┃</span>   ║
║  <span class="diagram-highlight">┃</span>  • Status Updates         <span class="diagram-highlight">┃</span>   ║
║  <span class="diagram-highlight">┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛</span>   ║
<span class="diagram-highlight">╚═══════════════╦═════════════════╝</span>
                <span class="diagram-highlight">▼</span>
<span class="diagram-highlight">╔═════════════════════════════════╗</span>
║      Redis (Task Queue)         ║
<span class="diagram-highlight">╚═══════════════╦═════════════════╝</span>
                <span class="diagram-highlight">▼</span>
<span class="diagram-highlight">╔═════════════════════════════════╗</span>
║     Celery Beat (Scheduling)    ║
<span class="diagram-highlight">╚═══════════════╦═════════════════╝</span>
                <span class="diagram-highlight">▼</span>
<span class="diagram-highlight">╔═════════════════════════════════╗</span>
║         Monitored Sites         ║
║                                 ║
║    Main     Backup    Staging   ║
<span class="diagram-highlight">╚═════════════════════════════════╝</span></pre>
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
  position: relative;
  overflow: hidden;
}

/* 太空背景元素样式 */
.stars {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: -2;
  pointer-events: none;
}

.star {
  position: absolute;
  background-color: white;
  border-radius: 50%;
  opacity: 0.4;
  animation: twinkle 4s infinite ease-in-out;
}

@keyframes twinkle {
  0%, 100% { opacity: 0.2; transform: scale(0.8); }
  50% { opacity: 0.7; transform: scale(1.2); }
}

.grid-lines {
  position: fixed;
  z-index: -1;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  opacity: 0.06;
  background-image: 
    linear-gradient(to right, var(--primary) 1px, transparent 1px),
    linear-gradient(to bottom, var(--primary) 1px, transparent 1px);
  background-size: 40px 40px;
  animation: grid-pulse 10s infinite ease-in-out;
}

@keyframes grid-pulse {
  0%, 100% { opacity: 0.04; }
  50% { opacity: 0.09; }
}

.planet-effect {
  position: fixed;
  width: 280px;
  height: 280px;
  top: -100px;
  right: -100px;
  background: radial-gradient(circle, rgba(42, 157, 143, 0.5) 0%, rgba(58, 134, 255, 0.3) 60%, transparent 100%);
  border-radius: 50%;
  box-shadow: inset 20px -20px 40px rgba(255, 255, 255, 0.4),
              inset -10px 10px 30px rgba(0, 0, 40, 0.6);
  z-index: -2;
  animation: planetRotate 60s infinite linear;
  filter: blur(4px);
}

@keyframes planetRotate {
  0% {
    box-shadow: inset 20px -20px 40px rgba(255, 255, 255, 0.4),
                inset -10px 10px 30px rgba(0, 0, 40, 0.6);
  }
  50% {
    box-shadow: inset -20px 20px 40px rgba(255, 255, 255, 0.4),
                inset 10px -10px 30px rgba(0, 0, 40, 0.6);
  }
  100% {
    box-shadow: inset 20px -20px 40px rgba(255, 255, 255, 0.4),
                inset -10px 10px 30px rgba(0, 0, 40, 0.6);
  }
}

.planet-ring {
  position: fixed;
  top: -120px;
  right: -120px;
  width: 320px;
  height: 320px;
  border-radius: 50%;
  z-index: -1;
  overflow: visible;
  transform: rotateX(75deg) rotateY(15deg);
  pointer-events: none;
  animation: orbitRotate 80s infinite linear;
}

@keyframes orbitRotate {
  from { transform: rotateX(75deg) rotateY(15deg) rotateZ(0deg); }
  to { transform: rotateX(75deg) rotateY(15deg) rotateZ(360deg); }
}

.planet-ring::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 280px;
  height: 280px;
  transform: translate(-50%, -50%);
  border: 10px solid rgba(251, 186, 114, 0.2);
  border-radius: 50%;
  box-shadow: 0 0 20px rgba(251, 186, 114, 0.4);
}

.planet-ring::after {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 240px;
  height: 240px;
  transform: translate(-50%, -50%);
  border: 6px solid rgba(58, 134, 255, 0.2);
  border-radius: 50%;
}

.orbital-path {
  position: fixed;
  top: 10%;
  left: -10%;
  width: 100vh;
  height: 100vh;
  border: 1px dashed rgba(58, 134, 255, 0.1);
  border-radius: 50%;
  animation: orbit-rotate 150s linear infinite;
  z-index: -1;
}

@keyframes orbit-rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.about-header {
  text-align: center;
  margin-bottom: 2.5rem;
  position: relative;
}

.about-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: relative;
}

.about-header h1::after {
  content: "";
  position: absolute;
  bottom: -8px;
  left: 50%;
  width: 80px;
  height: 3px;
  background: linear-gradient(to right, var(--primary), var(--primary-light));
  transform: translateX(-50%);
  border-radius: 3px;
  box-shadow: 0 0 10px rgba(58, 134, 255, 0.6);
}

.subtitle {
  font-size: 1.25rem;
  color: var(--text-secondary);
  max-width: 600px;
  margin: 1rem auto 0;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
  position: relative;
  z-index: 1;
}

.architecture-section {
  margin-top: 2rem;
  width: 100%;
  position: relative;
  z-index: 1;
}

.card {
  background: var(--bg-secondary);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 2rem;
  position: relative;
  transition: all 0.3s cubic-bezier(0.17, 0.67, 0.83, 0.67);
  height: 100%;
  display: flex;
  flex-direction: column;
  border: 1px solid var(--border-color);
  overflow: hidden;
  backdrop-filter: blur(5px);
}

/* Card space background effect */
.card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(58, 134, 255, 0.03) 0%, transparent 50%, rgba(42, 157, 143, 0.02) 100%);
  opacity: 0.6;
  z-index: -1;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
  border-color: rgba(58, 134, 255, 0.2);
}

/* Card glow effect */
.card::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: var(--radius);
  box-shadow: 0 0 30px rgba(58, 134, 255, 0.15);
  opacity: 0;
  transition: opacity 0.5s ease;
  z-index: -1;
}

.card:hover::after {
  opacity: 1;
}

.card-icon {
  width: 48px;
  height: 48px;
  margin-bottom: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  position: relative;
  overflow: hidden;
}

.card-icon::after {
  content: "";
  position: absolute;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at center, rgba(255, 255, 255, 0.2) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.card:hover .card-icon::after {
  opacity: 1;
}

.card-icon svg {
  width: 36px;
  height: 36px;
  transition: all 0.3s ease;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

.card:hover .card-icon svg {
  transform: scale(1.1);
  filter: drop-shadow(0 0 5px rgba(58, 134, 255, 0.4));
}

.feature-card .card-icon {
  background-color: rgba(42, 157, 143, 0.15);
  box-shadow: 0 0 15px rgba(42, 157, 143, 0.1);
}

.feature-card .card-icon svg {
  fill: var(--primary);
}

.architecture-card .card-icon {
  background-color: rgba(87, 115, 153, 0.15);
  box-shadow: 0 0 15px rgba(87, 115, 153, 0.1);
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
  position: relative;
  display: inline-block;
  left: 50%;
  transform: translateX(-50%);
}

.architecture-card h2::after {
  content: "";
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(to right, transparent, #577399, transparent);
  border-radius: 2px;
}

.architecture-diagram {
  width: 100%;
  overflow-x: auto;
  margin-bottom: 1.5rem;
  border: 1px solid rgba(58, 134, 255, 0.2);
  border-radius: var(--radius);
  background-color: rgba(0, 0, 30, 0.05);
  padding: 0.5rem;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1), inset 0 0 30px rgba(58, 134, 255, 0.05);
  position: relative;
  transition: all 0.3s ease;
}

.architecture-diagram:hover {
  border-color: rgba(58, 134, 255, 0.3);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15), inset 0 0 40px rgba(58, 134, 255, 0.08);
  transform: translateY(-2px);
}

/* Add subtle background animation */
.architecture-diagram::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 10% 20%, rgba(58, 134, 255, 0.03) 0%, transparent 50%),
    radial-gradient(circle at 90% 80%, rgba(42, 157, 143, 0.03) 0%, transparent 50%);
  opacity: 0.8;
  z-index: 0;
  pointer-events: none;
}

.diagram-text {
  font-family: 'Menlo', 'Monaco', 'Consolas', monospace;
  font-size: 0.95rem;
  line-height: 1.4;
  color: var(--text-primary);
  padding: 1.5rem;
  margin: 0;
  white-space: pre;
  position: relative;
  z-index: 1;
  overflow-x: auto;
  text-shadow: 0 0 1px rgba(58, 134, 255, 0.2);
}

/* Add subtle glow to special symbols */
.diagram-text .diagram-highlight {
  color: var(--primary);
  text-shadow: 0 0 3px rgba(58, 134, 255, 0.4);
}

.tech-card .card-icon {
  background-color: rgba(233, 196, 106, 0.15);
  box-shadow: 0 0 15px rgba(233, 196, 106, 0.1);
}

.tech-card .card-icon svg {
  fill: var(--secondary);
}

.metrics-card .card-icon {
  background-color: rgba(244, 162, 97, 0.15);
  box-shadow: 0 0 15px rgba(244, 162, 97, 0.1);
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
  position: relative;
  display: inline-block;
}

.card h2::after {
  content: "";
  position: absolute;
  bottom: -6px;
  left: 0;
  width: 60%;
  height: 2px;
  background: linear-gradient(to right, currentColor, transparent);
  border-radius: 2px;
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
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
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
  position: relative;
  display: inline-block;
}

.tech-item h3::after {
  content: "";
  position: absolute;
  bottom: -3px;
  left: 0;
  width: 70%;
  height: 1px;
  background: linear-gradient(to right, currentColor, transparent);
  border-radius: 1px;
}

.tech-item ul {
  padding-left: 1.25rem;
  margin: 0;
}

.tech-item li {
  margin-bottom: 0.5rem;
  color: var(--text-secondary);
  transition: transform 0.3s ease;
  position: relative;
}

.tech-item li:hover {
  transform: translateX(3px);
  color: var(--primary);
}

.metrics-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.metric-item {
  display: flex;
  align-items: flex-start;
  transition: transform 0.3s ease;
}

.metric-item:hover {
  transform: translateX(5px);
}

.metric-bullet {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: var(--primary);
  margin-top: 0.5rem;
  margin-right: 1rem;
  flex-shrink: 0;
  box-shadow: 0 0 8px rgba(58, 134, 255, 0.4);
  animation: pulse 3s infinite alternate;
}

@keyframes pulse {
  0% { box-shadow: 0 0 4px rgba(58, 134, 255, 0.3); }
  100% { box-shadow: 0 0 12px rgba(58, 134, 255, 0.6); }
}

.metric-item:nth-child(2) .metric-bullet {
  background-color: var(--secondary);
  box-shadow: 0 0 8px rgba(233, 196, 106, 0.4);
  animation-delay: 0.5s;
}

.metric-item:nth-child(3) .metric-bullet {
  background-color: var(--accent);
  box-shadow: 0 0 8px rgba(244, 162, 97, 0.4);
  animation-delay: 1s;
}

.metric-item:nth-child(4) .metric-bullet {
  background-color: var(--success);
  box-shadow: 0 0 8px rgba(34, 197, 94, 0.4);
  animation-delay: 1.5s;
}

.metric-item h3 {
  font-size: 1.1rem;
  margin: 0 0 0.25rem 0;
  color: var(--text-primary);
  font-weight: 600;
  transition: color 0.3s ease;
}

.metric-item:hover h3 {
  color: var(--primary);
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
  position: relative;
  z-index: 1;
}

.heart {
  color: #e74c3c;
  font-size: 1.1rem;
  display: inline-block;
  animation: heartbeat 1.5s infinite;
}

@keyframes heartbeat {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.2); }
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
  
  .planet-effect, .planet-ring {
    display: none;
  }
}

/* Additional explanation text */
.architecture-card p {
  text-align: center;
  font-size: 1.1rem;
  max-width: 800px;
  margin: 1rem auto 0;
  color: var(--text-secondary);
  line-height: 1.6;
  position: relative;
  z-index: 1;
}

.architecture-card p::after {
  content: "";
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 1px;
  background: linear-gradient(to right, transparent, var(--primary), transparent);
  opacity: 0.5;
}

/* Add floating animation to tech items on hover */
@keyframes float-item {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-3px); }
}

.tech-item li:hover {
  transform: translateX(3px);
  color: var(--primary);
  animation: float-item 2s ease-in-out infinite;
}
</style> 