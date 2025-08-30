import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import UploadCard from '../UploadCard.vue'

describe('UploadCard', () => {
  it('renders upload interface', () => {
    const wrapper = mount(UploadCard, {
      props: { isAnalyzing: false }
    })

    expect(wrapper.find('input[type="file"]')).toBeTruthy()
    expect(wrapper.text()).toContain('Analyze')
  })

  it('shows analyzing state', () => {
    const wrapper = mount(UploadCard, {
      props: { isAnalyzing: true }
    })

    expect(wrapper.text()).toContain('Analyzing')
  })

  it('emits analyze event on button click', async () => {
    const wrapper = mount(UploadCard, {
      props: { isAnalyzing: false }
    })

    // Simulate file selection via input
    const file = new File(['test'], 'test.json', { type: 'application/json' })
    const input = wrapper.find('input[type="file"]')
    Object.defineProperty(input.element, 'files', {
      value: [file],
      writable: false
    })
    await input.trigger('change')

    const button = wrapper.find('button')
    await button.trigger('click')
    expect(wrapper.emitted()).toHaveProperty('analyze')
  })

  it('handles file selection', async () => {
    const wrapper = mount(UploadCard, {
      props: { isAnalyzing: false }
    })

    const file = new File(['test'], 'test.json', { type: 'application/json' })
    const input = wrapper.find('input[type="file"]')
    
    Object.defineProperty(input.element, 'files', {
      value: [file],
      writable: false
    })

    await input.trigger('change')
    expect(wrapper.vm.selectedFile).toBe(file)
  })
})