import { ref, onMounted } from 'vue'

export function useDarkMode() {
  const isDarkMode = ref(false)

  const toggleDarkMode = () => {
    isDarkMode.value = !isDarkMode.value
    localStorage.setItem('darkMode', isDarkMode.value)
  }

  onMounted(() => {
    isDarkMode.value = localStorage.getItem('darkMode') === 'true'
  })

  return {
    isDarkMode,
    toggleDarkMode
  }
}