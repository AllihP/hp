import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],

  // Base = /static/ → tous les assets seront sous /static/assets/
  // Django les sert via WhiteNoise sans aucun conflit avec serve_spa
  base: '/static/',

  build: {
    outDir: 'dist',
    emptyOutDir: true,
  },

  server: {
    // En local : proxy /api et /media vers Django
    proxy: {
      '/api':   { target: 'http://localhost:8000', changeOrigin: true },
      '/media': { target: 'http://localhost:8000', changeOrigin: true },
      '/static': { target: 'http://localhost:8000', changeOrigin: true },
    }
  }
})
