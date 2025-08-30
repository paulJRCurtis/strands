import axios from 'axios'

export const analysisService = {
  async analyzeFile(file) {
    const formData = new FormData()
    formData.append('file', file)
    
    try {
      const response = await axios.post('/api/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        timeout: 30000
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
    const response = await axios.get(`/api/status/${jobId}`)
    return response.data
  }
}