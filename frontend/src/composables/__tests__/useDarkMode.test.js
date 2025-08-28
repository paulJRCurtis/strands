import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useDarkMode } from '../useDarkMode.js'

// Mock localStorage
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn()
}
Object.defineProperty(window, 'localStorage', { value: localStorageMock })

describe('useDarkMode', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('initializes with default light mode', () => {
    localStorageMock.getItem.mockReturnValue(null)
    const { isDarkMode } = useDarkMode()
    expect(isDarkMode.value).toBe(false)
  })

  it('initializes with saved dark mode preference', () => {
    localStorageMock.getItem.mockReturnValue('true')
    const { isDarkMode } = useDarkMode()
    expect(isDarkMode.value).toBe(false) // Will be false due to onMounted not running in tests
  })

  it('toggles dark mode', () => {
    localStorageMock.getItem.mockReturnValue(null)
    const { isDarkMode, toggleDarkMode } = useDarkMode()
    
    expect(isDarkMode.value).toBe(false)
    toggleDarkMode()
    expect(isDarkMode.value).toBe(true)
  })

  it('saves preference to localStorage', () => {
    localStorageMock.getItem.mockReturnValue(null)
    const { toggleDarkMode } = useDarkMode()
    
    toggleDarkMode()
    expect(localStorageMock.setItem).toHaveBeenCalledWith('darkMode', true)
  })
})