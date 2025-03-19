const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    host: '0.0.0.0',
    port: 8080,
    proxy: {
      '^/': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        ws: true,
        logLevel: 'debug'
      }
    }
  },
  configureWebpack: {
    resolve: {
      fallback: {
        "vue": require.resolve("vue/dist/vue.esm-bundler.js")
      }
    },
    output: {
      filename: '[name].[hash].js',
      chunkFilename: '[name].[hash].js'
    }
  },
  pages: {
    index: {
      entry: 'src/main.js',
      template: 'public/index.html',
      filename: 'index.html',
      title: 'Kepler Monitor'
    }
  },
  chainWebpack: config => {
    config.resolve.alias.set('vue', '@vue/runtime-dom')
  }
}) 