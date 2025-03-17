<template>
  <div id="app">
    <header>
      <h1>Tofu Monitor</h1>
      <nav>
        <router-link to="/">Dashboard</router-link> |
        <router-link to="/metrics">Metrics</router-link> |
        <router-link to="/about">About</router-link>
      </nav>
    </header>
    <main>
      <router-view/>
    </main>
    <footer>
      <p>Tofu Monitor &copy; {{ new Date().getFullYear() }}</p>
    </footer>
  </div>
</template>

<style>
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu,
    Cantarell, 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f5f7fa;
  color: #333;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

header {
  background-color: #2c3e50;
  color: white;
  padding: 1rem;
  text-align: center;
}

header h1 {
  margin: 0 0 1rem 0;
}

nav {
  margin-bottom: 1rem;
}

nav a {
  color: #9cb3c9;
  text-decoration: none;
  padding: 0.5rem;
  border-radius: 4px;
  transition: all 0.3s ease;
  margin: 0 0.5rem;
}

nav a.router-link-active {
  color: white;
  font-weight: bold;
}

main {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;
}

footer {
  background-color: #2c3e50;
  color: white;
  text-align: center;
  padding: 1rem;
  margin-top: auto;
}
</style> 