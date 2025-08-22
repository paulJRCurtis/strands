import axios from 'axios'

const API_BASE_URL = 'http://localhost:8001'

export const analysisService = {
  async analyzeFile(file) {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await axios.post(`${API_BASE_URL}/analyze`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    return response.data
  },

  async getJobStatus(jobId) {
    const response = await axios.get(`${API_BASE_URL}/status/${jobId}`)
    return response.data
  }
}