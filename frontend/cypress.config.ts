import { defineConfig } from 'cypress'
import coverage from '@cypress/code-coverage/task'

export default defineConfig({
  e2e: {
    specPattern: 'cypress/e2e/**/*.{cy,spec}.{js,jsx,ts,tsx}',
    baseUrl: 'http://localhost:4173',
    setupNodeEvents(on, config) {
      coverage(on, config)
    }
  }
})
