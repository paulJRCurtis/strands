import { ref } from 'vue'

export function useFileUpload() {
  const selectedFile = ref(null)
  const isDragOver = ref(false)

  const handleFileUpload = (event) => {
    selectedFile.value = event.target.files[0]
  }

  const handleDrop = (event) => {
    isDragOver.value = false
    const files = event.dataTransfer.files
    if (files.length > 0) {
      selectedFile.value = files[0]
    }
  }

  return {
    selectedFile,
    isDragOver,
    handleFileUpload,
    handleDrop
  }
}