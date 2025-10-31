import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],

  // Add this 'server' block
  server: {
    proxy: {
      // This will proxy any request starting with /api
      '/api': {
        target: 'http://192.168.1.13', // Your Fedora VM's IP
        changeOrigin: true, // Needed for virtual hosted sites
        secure: false,      // If you're not using HTTPS
      }
    }
  }
})