const { defineConfig } = require('@vue/cli-service')
const MonacoWebpackPlugin = require('monaco-editor-webpack-plugin')

module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    plugins: [
      new MonacoWebpackPlugin({
        languages: ['json']
      })
    ]
  },
  devServer: {
    port: 8080,
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        ws: true
      }
    }
  }
}) 