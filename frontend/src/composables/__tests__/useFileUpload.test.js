import { describe, it, expect } from 'vitest'
import { useFileUpload } from '../useFileUpload.js'

describe('useFileUpload', () => {
  it('initializes with null selected file', () => {
    const { selectedFile, isDragOver } = useFileUpload()
    expect(selectedFile.value).toBe(null)
    expect(isDragOver.value).toBe(false)
  })

  it('handles file upload', () => {
    const { selectedFile, handleFileUpload } = useFileUpload()
    const file = new File(['test'], 'test.json', { type: 'application/json' })
    
    const mockEvent = {
      target: { files: [file] }
    }
    
    handleFileUpload(mockEvent)
    expect(selectedFile.value).toBe(file)
  })

  it('handles drag and drop', () => {
    const { selectedFile, isDragOver, handleDrop } = useFileUpload()
    const file = new File(['test'], 'test.json', { type: 'application/json' })
    
    const mockEvent = {
      dataTransfer: { files: [file] }
    }
    
    handleDrop(mockEvent)
    expect(selectedFile.value).toBe(file)
    expect(isDragOver.value).toBe(false)
  })

  it('handles empty drop', () => {
    const { selectedFile, handleDrop } = useFileUpload()
    
    const mockEvent = {
      dataTransfer: { files: [] }
    }
    
    handleDrop(mockEvent)
    expect(selectedFile.value).toBe(null)
  })
})