<template>
  <div class="upload-card">
    <h2>Upload Architecture</h2>
    <div class="upload-area" :class="{ 'drag-over': isDragOver }" 
         @dragover.prevent="isDragOver = true" 
         @dragleave="isDragOver = false" 
         @drop.prevent="handleDrop">
      <input type="file" @change="handleFileUpload" accept=".json,.yml,.yaml,.md" class="file-input" id="file-input">
      <label for="file-input" class="upload-label">
        <div class="upload-icon">📁</div>
        <p>{{ selectedFile ? selectedFile.name : 'Drop files here or click to browse' }}</p>
        <p class="file-types">Supports JSON, YAML, Markdown files</p>
      </label>
    </div>
    <button @click="$emit('analyze')" :disabled="!selectedFile" class="analyze-btn">
      <span v-if="isAnalyzing">🔄 Analyzing...</span>
      <span v-else>🔍 Analyze Architecture</span>
    </button>
  </div>
</template>

<script>
import { useFileUpload } from '../composables/useFileUpload.js'

export default {
  name: 'UploadCard',
  props: {
    isAnalyzing: Boolean
  },
  emits: ['analyze'],
  setup(props, { expose }) {
    const { selectedFile, isDragOver, handleFileUpload, handleDrop } = useFileUpload()
    
    // Expose selectedFile to parent component
    expose({ selectedFile })
    
    return {
      selectedFile,
      isDragOver,
      handleFileUpload,
      handleDrop
    }
  }
}
</script>