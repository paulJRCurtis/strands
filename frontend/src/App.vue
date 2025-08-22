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
      <UploadCard :isAnalyzing="isAnalyzing" @analyze="analyzeFile" ref="uploadCard" />
      <ResultsCard v-if="analysisResult" :analysisResult="analysisResult" />
    </main>
  </div>
</template>

<script>
import './styles.css'
import { useDarkMode } from './composables/useDarkMode.js'
import { analysisService } from './services/analysisService.js'
import UploadCard from './components/UploadCard.vue'
import ResultsCard from './components/ResultsCard.vue'

export default {
  name: 'App',
  components: {
    UploadCard,
    ResultsCard
  },
  setup() {
    const { isDarkMode, toggleDarkMode } = useDarkMode()
    return {
      isDarkMode,
      toggleDarkMode
    }
  },
  data() {
    return {
      analysisResult: null,
      isAnalyzing: false
    }
  },
  methods: {
    async analyzeFile() {
      const selectedFile = this.$refs.uploadCard?.selectedFile
      
      if (!selectedFile) return
      
      this.isAnalyzing = true
      console.log('Sending file:', selectedFile.name)
      
      try {
        const response = await analysisService.analyzeFile(selectedFile)
        console.log('Full response:', response)
        
        this.analysisResult = response.report
        
        console.log('Analysis result set:', this.analysisResult)
        console.log('Findings by severity:', this.analysisResult?.findings_by_severity)
      } catch (error) {
        console.error('Analysis failed:', error)
        console.error('Error details:', error.response?.data)
        alert('Analysis failed: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.isAnalyzing = false
      }
    }

  }
}
</script>