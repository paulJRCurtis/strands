import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  test: {
    environment: 'jsdom',
    exclude: [
      // '**/user.lib.python/**',
      '**/node_modules/**',
      '**/dist/**',
      '**/tests/e2e/**'
    ],
    outputFile: {
      junit: './test-results/junit.xml'
    },
    coverage: {
      reportsDirectory: './test-results',
      // reporter: ['text', 'json', 'html', 'lcov'],
      reporter: ['cobertura'],
      // outputFile: {
      //   junit: './test-results/junit.xml'
      // },
      exclude: [
        '**/user.lib.python/**',
        'node_modules/',
        'dist/',
        '**/*.config.js',
        '**/*.config.ts',
        '**/tests/**',
        '**/.eslintrc.cjs',
        '**/test-results/**'
      ]
    }
  }
})