import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'https://parkwise-ai-vb7g.onrender.com',
        changeOrigin: true,
      },
      '/health': {
        target: 'https://parkwise-ai-vb7g.onrender.com',
        changeOrigin: true,
      },
    },
  },
})
