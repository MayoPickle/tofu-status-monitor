<template>
  <div class="slide">
    <h1 class="title">What is Cursor?</h1>
    
    <div class="content">
      <div class="description">
        <h2>The AI-first code editor</h2>
        <p>Cursor is a code editor with AI built-in from the ground up, designed to help developers write, understand, and improve code faster than ever before.</p>
        <p>With Cursor, you can:</p>
        <ul>
          <li>Generate code with AI assistance</li>
          <li>Explain complex code with natural language</li>
          <li>Debug issues with AI-powered analysis</li>
          <li>Refactor code quickly and accurately</li>
        </ul>
        
        <div class="features">
          <div class="feature">
            <h3>AI-Powered Productivity</h3>
            <p>Write and edit code at unprecedented speeds with AI that understands your codebase context.</p>
          </div>
          
          <div class="feature">
            <h3>Built for Developers</h3>
            <p>Designed with developer workflows in mind, featuring intuitive commands and keyboard shortcuts.</p>
          </div>
        </div>
        
        <div class="mcp-info">
          <h3>About MCP Service</h3>
          <p>MCP (Managed Cursor Platform) provides enterprise-grade management, security, and collaboration features for teams using Cursor.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CursorIntroSlide'
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

.content {
  display: flex;
  flex: 1;
  justify-content: center;
}

.description {
  max-width: 800px;
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  color: #3498db;
  margin-bottom: 1rem;
}

h3 {
  color: #3498db;
  margin-bottom: 0.5rem;
}

ul {
  margin-bottom: 1.5rem;
}

li {
  margin-bottom: 0.5rem;
}

.features {
  display: flex;
  gap: 1rem;
  margin: 1.5rem 0;
}

.feature {
  flex: 1;
  background-color: #f5f5f5;
  padding: 1rem;
  border-radius: 6px;
}

.mcp-info {
  margin-top: 1.5rem;
  padding: 1rem;
  background-color: #f5f5f5;
  border-radius: 6px;
}
</style> 