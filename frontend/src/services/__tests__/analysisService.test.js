import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'
import { analysisService } from '../analysisService'

vi.mock('axios')

describe('analysisService', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('analyzes file successfully', async () => {
    const mockResponse = {
      data: {
        job_id: 'test-123',
        status: 'completed',
        findings: [],
        risk_score: 50
      }
    }
    
    axios.post.mockResolvedValue(mockResponse)
    
    const file = new File(['test'], 'test.json', { type: 'application/json' })
    const result = await analysisService.analyzeFile(file)
    
    expect(axios.post).toHaveBeenCalledWith(
      '/api/analyze',
      expect.any(FormData),
      { headers: { 'Content-Type': 'multipart/form-data' } }
    )
    expect(result).toEqual(mockResponse.data)
  })

  it('gets job status successfully', async () => {
    const mockResponse = {
      data: { job_id: 'test-123', status: 'completed' }
    }
    
    axios.get.mockResolvedValue(mockResponse)
    
    const result = await analysisService.getJobStatus('test-123')
    
    expect(axios.get).toHaveBeenCalledWith('/api/status/test-123')
    expect(result).toEqual(mockResponse.data)
  })
})