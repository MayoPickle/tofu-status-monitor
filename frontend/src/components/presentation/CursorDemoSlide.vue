<template>
  <div class="slide">
    <h1 class="title">Development Demo</h1>
    
    <div class="demo-container">
      <div class="timeline">
        <div class="timeline-header">
          <h2>From Idea to Product in 3.5 Days</h2>
          <p>This presentation itself was created using Cursor!</p>
        </div>
        
        <div class="timeline-steps">
          <div class="timeline-step">
            <div class="step-date">Day 1</div>
            <div class="step-content">
              <h3>Initial Concept</h3>
              <p>Project idea conceptualized on the evening of the 18th</p>
              <ul>
                <li>Defined requirements and goals</li>
                <li>Sketched basic architecture</li>
                <li>Set up project scaffolding</li>
              </ul>
            </div>
          </div>
          
          <div class="timeline-step">
            <div class="step-date">Day 2</div>
            <div class="step-content">
              <h3>Core Development</h3>
              <p>Built the foundation and key components</p>
              <ul>
                <li>Implemented data layer</li>
                <li>Created main interface</li>
                <li>Set up business logic</li>
              </ul>
            </div>
          </div>
          
          <div class="timeline-step">
            <div class="step-date">Day 3</div>
            <div class="step-content">
              <h3>Feature Completion</h3>
              <p>Added all planned features and testing</p>
              <ul>
                <li>Implemented remaining features</li>
                <li>Added responsive design</li>
                <li>Conducted initial testing</li>
              </ul>
            </div>
          </div>
          
          <div class="timeline-step">
            <div class="step-date">Day 3.5</div>
            <div class="step-content">
              <h3>Final Polish</h3>
              <p>Refined the application to near production quality</p>
              <ul>
                <li>Bug fixes and optimizations</li>
                <li>UI/UX improvements</li>
                <li>Final review and documentation</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      
      <div class="productivity-stats">
        <h2>Productivity Stats</h2>
        <div class="stat-cards">
          <div class="stat-card">
            <div class="stat-value">3.5 days</div>
            <div class="stat-label">Total Development Time</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">~14 days</div>
            <div class="stat-label">Estimated Time Without Cursor</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">75%</div>
            <div class="stat-label">Time Saved</div>
          </div>
        </div>
        
        <div class="conclusion">
          <p>What would normally take 2+ weeks was completed in just 3.5 days with Cursor's AI assistance.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CursorDemoSlide'
}
</script>

<style scoped>
.slide {
  height: 100%;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  background-color: #f9f9f9;
}

.title {
  text-align: center;
  margin-bottom: 2rem;
  color: #2c3e50;
  font-size: 2.5rem;
}

.demo-container {
  display: flex;
  flex-direction: column;
  flex: 1;
  gap: 2rem;
}

.timeline {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.timeline-header {
  margin-bottom: 1.5rem;
  text-align: center;
}

.timeline-header h2 {
  color: #3498db;
  margin-bottom: 0.5rem;
}

.timeline-steps {
  display: flex;
  justify-content: space-between;
  position: relative;
}

.timeline-steps::before {
  content: '';
  position: absolute;
  top: 35px;
  left: 50px;
  right: 50px;
  height: 4px;
  background-color: #3498db;
  z-index: 0;
}

.timeline-step {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 1;
}

.step-date {
  background-color: #3498db;
  color: white;
  border-radius: 30px;
  padding: 0.5rem 1rem;
  font-weight: bold;
  margin-bottom: 1rem;
  text-align: center;
  min-width: 100px;
}

.step-content {
  background-color: #f5f5f5;
  border-radius: 8px;
  padding: 1rem;
  width: 90%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.step-content h3 {
  color: #3498db;
  margin-bottom: 0.5rem;
}

.step-content ul {
  padding-left: 1.2rem;
  margin-top: 0.5rem;
}

.step-content li {
  margin-bottom: 0.3rem;
  font-size: 0.9rem;
}

.productivity-stats {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.productivity-stats h2 {
  color: #3498db;
  margin-bottom: 1.5rem;
  text-align: center;
}

.stat-cards {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat-card {
  flex: 1;
  background-color: #f5f5f5;
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stat-value {
  font-size: 1.8rem;
  font-weight: bold;
  color: #3498db;
  margin-bottom: 0.5rem;
}

.conclusion {
  text-align: center;
  font-size: 1.2rem;
  font-weight: bold;
  margin-top: 1rem;
}
</style> 