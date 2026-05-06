import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    host: '0.0.0.0', 
    port: 5173,
    open: false, // 建议设为 false，防止穿透时自动打开本地浏览器
    allowedHosts: true, // 关键：允许所有主机头（包括 cloudflare 的随机域名）
    proxy: {
      '/api': {
        target: 'http://localhost:5000', // 尝试将 127.0.0.1 改为 localhost
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''), // 【重要】去掉 /api 前缀再发给后端
        // 如果后端确实需要 /api 前缀，请注释掉上面这行 rewrite
        secure: false, // 如果后端是 https 自签名证书，需要此项
        ws: true,      // 如果需要支持 WebSocket
      }
    }
  }
})