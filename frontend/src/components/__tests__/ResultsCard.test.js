import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import ResultsCard from '../ResultsCard.vue'

describe('ResultsCard', () => {
  const mockAnalysisResult = {
    summary: 'Test analysis completed',
    total_findings: 3,
    risk_score: 75,
    findings_by_severity: {
      HIGH: [{ description: 'High severity issue' }],
      MEDIUM: [{ description: 'Medium severity issue' }],
      LOW: [{ description: 'Low severity issue' }]
    },
    recommendations: ['Fix issue 1', 'Fix issue 2']
  }

  it('renders analysis results correctly', () => {
    const wrapper = mount(ResultsCard, {
      props: { analysisResult: mockAnalysisResult }
    })

    expect(wrapper.text()).toContain('Test analysis completed')
    expect(wrapper.text()).toContain('75/100')
    expect(wrapper.text()).toContain('3')
  })

  it('displays correct risk score class', () => {
    const wrapper = mount(ResultsCard, {
      props: { analysisResult: mockAnalysisResult }
    })

    expect(wrapper.vm.getRiskScoreClass(75)).toBe('high-risk')
    expect(wrapper.vm.getRiskScoreClass(50)).toBe('medium-risk')
    expect(wrapper.vm.getRiskScoreClass(20)).toBe('low-risk')
  })

  it('shows recommendations when available', () => {
    const wrapper = mount(ResultsCard, {
      props: { analysisResult: mockAnalysisResult }
    })

    expect(wrapper.text()).toContain('Fix issue 1')
    expect(wrapper.text()).toContain('Fix issue 2')
  })
})