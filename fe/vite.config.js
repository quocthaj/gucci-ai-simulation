import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Dev proxy: forward /chat to FastAPI on port 8000
    proxy: {
      '/chat': 'http://127.0.0.1:8000',
      '/docs': 'http://127.0.0.1:8000',
    }
  },
  build: {
    // Output to ../fe/dist so FastAPI can serve from there
    outDir: 'dist',
  }
})
