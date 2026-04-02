import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],

  build: {
    outDir: 'dist',
    // Optimisation pour la production
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom'],
          i18n:   ['i18next', 'react-i18next'],
        }
      }
    }
  },

  // En production, l'API est sur le backend Render
  // La variable VITE_API_URL est définie dans Render → Environment
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
