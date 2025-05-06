import axios from 'axios'

const axiosClient = axios.create({
  baseURL: process.env.REACT_APP_BACKEND_SERVICE_URL, // Replace with actual backend URL
  headers: {
    'Content-Type': 'application/json',
  },
})

// Optional: Add interceptors for logging or auth
axiosClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export default axiosClient
