import axios from 'axios'

// Robust API URL detection
function getApiBaseUrl() {
  // 1. Use explicit environment variable if set
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL
  }
  
  // 2. Use relative path if same origin (production)
  if (window.location.hostname !== 'localhost') {
    return window.location.origin
  }
  
  // 3. Default to localhost for development
  return 'http://localhost:8000'
}

const API_BASE_URL = getApiBaseUrl()

export const analysisService = {
  async analyzeFile(file) {
    const formData = new FormData()
    formData.append('file', file)
    
    try {
      const response = await axios.post(`${API_BASE_URL}/analyze`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        timeout: 30000 // 30 second timeout
      })
      
      return response.data
    } catch (error) {
      if (error.code === 'ECONNREFUSED' || error.code === 'ERR_NETWORK') {
        throw new Error('Backend service is not available. Please check if the coordinator is running.')
      }
      throw error
    }
  },

  async getJobStatus(jobId) {
    const response = await axios.get(`${API_BASE_URL}/status/${jobId}`)
    return response.data
  }
}