<template>
  <div class="results-card">
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
        <FindingCard 
          v-if="Array.isArray(findingsList) && findingsList.length > 0"
          :severity="severity"
          :findings="findingsList"
        />
      </template>
    </div>
  </div>
</template>

<script>
import FindingCard from './FindingCard.vue'

export default {
  name: 'ResultsCard',
  components: {
    FindingCard
  },
  props: {
    analysisResult: Object
  },
  methods: {
    getRiskScoreClass(score) {
      if (score >= 70) return 'high-risk'
      if (score >= 40) return 'medium-risk'
      return 'low-risk'
    }
  }
}
</script>