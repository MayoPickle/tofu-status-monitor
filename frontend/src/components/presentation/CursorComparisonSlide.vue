<template>
  <div class="slide">
    <h1 class="title">Cursor vs Other AI Tools</h1>
    
    <div class="comparison-container">
      <div class="comparison-card">
        <div class="card-header cursor">
          <h2>Cursor</h2>
          <div class="efficiency">
            <span class="percentage">2000%</span>
            <span class="label">Efficiency Boost</span>
          </div>
        </div>
        <div class="card-content">
          <ul>
            <li><strong>Integrated AI:</strong> Built from the ground up with AI in mind</li>
            <li><strong>Context-aware:</strong> Understands the entire codebase</li>
            <li><strong>Specialized for coding:</strong> Optimized specifically for software development</li>
            <li><strong>Faster workflow:</strong> Streamlined UI for quick development</li>
            <li><strong>Code execution:</strong> Can run and debug code directly</li>
            <li><strong>Project understanding:</strong> Comprehends project structure</li>
          </ul>
        </div>
      </div>
      
      <div class="vs">VS</div>
      
      <div class="comparison-card">
        <div class="card-header chatgpt">
          <h2>ChatGPT / Copilot</h2>
          <div class="efficiency">
            <span class="percentage">500%</span>
            <span class="label">Efficiency Boost</span>
          </div>
        </div>
        <div class="card-content">
          <ul>
            <li><strong>General purpose:</strong> Designed for multiple use cases</li>
            <li><strong>Limited context:</strong> May not understand entire codebase</li>
            <li><strong>Add-on approach:</strong> Integrated into existing editors</li>
            <li><strong>More context switching:</strong> Often requires switching windows</li>
            <li><strong>Text generation:</strong> Focused on generating text/code snippets</li>
            <li><strong>File-level focus:</strong> Often works with one file at a time</li>
          </ul>
        </div>
      </div>
    </div>
    
    <div class="conclusion">
      <p>Cursor provides a <span class="highlight">4x productivity improvement</span> compared to other AI coding tools by being specifically designed for software development from the ground up.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CursorComparisonSlide'
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

.comparison-container {
  display: flex;
  flex: 1;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.comparison-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  max-width: 45%;
}

.card-header {
  padding: 1.5rem;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.cursor {
  background-color: #3498db;
}

.chatgpt {
  background-color: #16a085;
}

.efficiency {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.percentage {
  font-size: 2rem;
  font-weight: bold;
}

.label {
  font-size: 0.9rem;
}

.card-content {
  padding: 1.5rem;
  flex: 1;
}

.vs {
  font-size: 2rem;
  font-weight: bold;
  color: #7f8c8d;
}

ul {
  padding-left: 1.5rem;
}

li {
  margin-bottom: 0.75rem;
}

.conclusion {
  margin-top: 2rem;
  text-align: center;
  font-size: 1.25rem;
}

.highlight {
  background-color: #fff176;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-weight: bold;
}
</style> 