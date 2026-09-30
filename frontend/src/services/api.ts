import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://172.30.224.1:8000/api/v1'

// Debug log
if (typeof window !== 'undefined') {
  console.log('API_BASE_URL:', API_BASE_URL)
  console.log('VITE_API_URL env:', import.meta.env.VITE_API_URL)
}

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add request interceptor for auth tokens
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api
