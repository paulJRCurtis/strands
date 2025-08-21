<template>
  <div id="app" :class="{ 'dark-mode': isDarkMode }">
    <header class="header">
      <div class="header-content">
        <h1 class="title">🛡️ Security Analysis Platform</h1>
        <button @click="toggleDarkMode" class="theme-toggle">
          {{ isDarkMode ? '☀️' : '🌙' }}
        </button>
      </div>
    </header>
    
    <main class="main">
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
        <button @click="analyzeFile" :disabled="!selectedFile" class="analyze-btn">
          <span v-if="isAnalyzing">🔄 Analyzing...</span>
          <span v-else>🔍 Analyze Architecture</span>
        </button>
      </div>
      
      <div v-if="analysisResult" class="results-card">
        <div class="results-header">
          <h2>Analysis Results</h2>
          <div class="risk-score" :class="getRiskScoreClass(analysisResult.risk_score)">
            {{ analysisResult.risk_score }}/100
          </div>
        </div>
        
        <div class="summary-card">
          <p class="summary-text">{{ analysisResult.summary }}</p>
          <div class="stats">
            <div class="stat">
              <span class="stat-number">{{ analysisResult.total_findings }}</span>
              <span class="stat-label">Total Issues</span>
            </div>
          </div>
        </div>
        

        
        <div v-if="analysisResult.recommendations && analysisResult.recommendations.length > 0" class="recommendations-card">
          <h3>🔧 Security Recommendations</h3>
          <ul class="recommendations-list">
            <li v-for="recommendation in analysisResult.recommendations" :key="recommendation" class="recommendation-item">
              {{ recommendation }}
            </li>
          </ul>
        </div>
        

        
        <div class="findings-grid" v-if="analysisResult && analysisResult.findings_by_severity">
          <template v-for="(findingsList, severity) in analysisResult.findings_by_severity" :key="severity">
            <div v-if="Array.isArray(findingsList) && findingsList.length > 0" class="severity-card" :class="severity.toLowerCase()">
              <div class="severity-header">
                <span class="severity-badge">{{ getSeverityIcon(severity) }} {{ severity }}</span>
                <span class="count">{{ findingsList.length }}</span>
              </div>
              <div class="findings-list">
                <div v-for="finding in findingsList" :key="finding.description" class="finding-item">
                  <div class="finding-header">
                    <div class="finding-description">{{ finding.description }}</div>
                    <div class="finding-category">{{ finding.category }}</div>
                  </div>
                  <div class="finding-details">
                    <div class="finding-recommendation">
                      <span class="icon">💡</span>
                      <span class="label">Recommendation:</span>
                      <span class="text">{{ finding.recommendation }}</span>
                    </div>
                    <div class="finding-component">
                      <span class="icon">📍</span>
                      <span class="label">Affected Component:</span>
                      <span class="text">{{ finding.affected_component }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </template>
        </div>

      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios'
import './styles.css'

export default {
  name: 'App',
  data() {
    return {
      selectedFile: null,
      analysisResult: null,
      isDarkMode: false,
      isDragOver: false,
      isAnalyzing: false
    }
  },
  mounted() {
    this.isDarkMode = localStorage.getItem('darkMode') === 'true'
  },
  methods: {
    handleFileUpload(event) {
      console.log('File upload triggered', event.target.files)
      this.selectedFile = event.target.files[0]
      console.log('Selected file:', this.selectedFile)
    },
    handleDrop(event) {
      console.log('Drop event triggered', event.dataTransfer.files)
      this.isDragOver = false
      const files = event.dataTransfer.files
      if (files.length > 0) {
        this.selectedFile = files[0]
        console.log('Selected file via drop:', this.selectedFile)
      }
    },
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode
      localStorage.setItem('darkMode', this.isDarkMode)
    },
    async analyzeFile() {
      if (!this.selectedFile) return
      
      this.isAnalyzing = true
      const formData = new FormData()
      formData.append('file', this.selectedFile)
      
      console.log('Sending file:', this.selectedFile.name)
      
      try {
        const response = await axios.post('http://localhost:8001/analyze', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        console.log('Full response:', response.data)
        
        // Always use the report from response.data.report
        this.analysisResult = response.data.report
        
        console.log('Analysis result set:', this.analysisResult)
        console.log('Findings by severity:', this.analysisResult?.findings_by_severity)
      } catch (error) {
        console.error('Analysis failed:', error)
        console.error('Error details:', error.response?.data)
        alert('Analysis failed: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.isAnalyzing = false
      }
    },
    getRiskScoreClass(score) {
      if (score >= 70) return 'high-risk'
      if (score >= 40) return 'medium-risk'
      return 'low-risk'
    },
    getSeverityIcon(severity) {
      const icons = {
        'CRITICAL': '🚨',
        'HIGH': '⚠️',
        'MEDIUM': '⚡',
        'LOW': 'ℹ️'
      }
      return icons[severity] || '•'
    }
  }
}
</script>