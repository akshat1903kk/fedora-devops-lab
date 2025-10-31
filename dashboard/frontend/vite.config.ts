import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],

  // Add this 'server' block
  server: {
  proxy: {
    '/api': {
      target: 'http://192.168.1.13:8080', // <-- CHANGE THIS PORT
      changeOrigin: true,
      secure: false,
    }
  }
}
})