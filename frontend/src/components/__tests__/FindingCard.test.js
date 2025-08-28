import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import FindingCard from '../FindingCard.vue'

describe('FindingCard', () => {
  const mockFindings = [
    {
      description: 'Test security issue',
      category: 'Network Security',
      recommendation: 'Fix this issue',
      affected_component: 'Web Server'
    }
  ]

  it('renders findings correctly', () => {
    const wrapper = mount(FindingCard, {
      props: {
        severity: 'HIGH',
        findings: mockFindings
      }
    })

    expect(wrapper.text()).toContain('Test security issue')
    expect(wrapper.text()).toContain('Network Security')
    expect(wrapper.find('.severity-badge').text()).toContain('HIGH')
  })

  it('displays correct severity icon', () => {
    const wrapper = mount(FindingCard, {
      props: {
        severity: 'CRITICAL',
        findings: mockFindings
      }
    })

    expect(wrapper.vm.getSeverityIcon('CRITICAL')).toBe('🚨')
    expect(wrapper.vm.getSeverityIcon('HIGH')).toBe('⚠️')
  })

  it('shows findings count', () => {
    const wrapper = mount(FindingCard, {
      props: {
        severity: 'MEDIUM',
        findings: mockFindings
      }
    })

    expect(wrapper.find('.count').text()).toBe('1')
  })
})