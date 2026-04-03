import axios from 'axios'

// En production (Render) : VITE_API_URL=/api → même domaine
// En local : VITE_API_URL=http://localhost:8000/api
const API_BASE = import.meta.env.VITE_API_URL || '/api'

const api = axios.create({ baseURL: API_BASE })

export const getProfile  = () => api.get('/profile/')
export const getSkills   = () => api.get('/skills/')
export const getCV       = () => api.get('/cv/')
export const getArticles = () => api.get('/articles/')
export const sendContact = (data) => api.post('/contact/', data)

export const getField = (obj, lang, field) => {
  if (!obj) return ''
  return obj[`${field}_${lang}`] || obj[`${field}_fr`] || ''
}
