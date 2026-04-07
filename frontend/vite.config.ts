import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      // 使用 fileURLToPath 方式（Vite 推荐）
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 5173,  // 默认端口，可修改
    open: true,  // 启动时自动打开浏览器
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        // 如果需要重写路径，可以添加：
        // rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})