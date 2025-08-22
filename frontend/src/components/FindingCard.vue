<template>
  <div class="severity-card" :class="severity.toLowerCase()">
    <div class="severity-header">
      <span class="severity-badge">{{ getSeverityIcon(severity) }} {{ severity }}</span>
      <span class="count">{{ findings.length }}</span>
    </div>
    <div class="findings-list">
      <div v-for="finding in findings" :key="finding.description" class="finding-item">
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

<script>
export default {
  name: 'FindingCard',
  props: {
    severity: String,
    findings: Array
  },
  methods: {
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