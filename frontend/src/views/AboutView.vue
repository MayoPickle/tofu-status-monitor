<template>
  <div class="about">
    <h1>About Tofu Monitor</h1>
    
    <div class="card">
      <h2>Project Overview</h2>
      <p>
        Tofu Monitor is a status monitoring application designed to track the performance and availability
        of the <code>https://yudoufu.org/tofu/rooms/</code> endpoint. The system performs regular checks every 
        60 seconds to ensure the endpoint is running properly and collects performance metrics.
      </p>
    </div>
    
    <div class="card">
      <h2>Technologies Used</h2>
      <ul>
        <li><strong>Backend:</strong> FastAPI, Celery, PostgreSQL, Redis</li>
        <li><strong>Frontend:</strong> Vue.js, Chart.js</li>
      </ul>
      <p>
        The backend uses Celery to schedule regular monitoring tasks with Redis as the message broker.
        All metrics are stored in PostgreSQL for long-term analysis. The frontend provides visualizations
        and real-time updates of the collected data.
      </p>
    </div>
    
    <div class="card">
      <h2>Metrics Collected</h2>
      <ul>
        <li><strong>Request Duration:</strong> Time taken to complete each request</li>
        <li><strong>Status Codes:</strong> HTTP status codes returned by the endpoint</li>
        <li><strong>Weekly Averages:</strong> Average response time calculated on a weekly basis</li>
        <li><strong>Success Rate:</strong> Percentage of successful requests</li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.about {
  max-width: 100%;
}

.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.card h2 {
  margin-top: 0;
  margin-bottom: 1rem;
  font-size: 1.25rem;
  color: #2c3e50;
}

ul {
  padding-left: 1.5rem;
}

li {
  margin-bottom: 0.5rem;
}

code {
  background-color: #f5f7fa;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  font-family: monospace;
  font-size: 0.9em;
}
</style> 