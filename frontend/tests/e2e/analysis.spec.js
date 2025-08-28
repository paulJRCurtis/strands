import { test, expect } from '@playwright/test'

test.describe('Security Analysis Platform', () => {
  test('should upload file and display results', async ({ page }) => {
    await page.goto('http://localhost:3000')
    
    // Check page title
    await expect(page).toHaveTitle(/Security Analysis Platform/)
    
    // Upload file
    const fileInput = page.locator('input[type="file"]')
    await fileInput.setInputFiles('../../example_architecture.md')
    
    // Click analyze button
    await page.click('button:has-text("Analyze")')
    
    // Wait for results
    await expect(page.locator('.results-card')).toBeVisible({ timeout: 10000 })
    
    // Check findings are displayed
    await expect(page.locator('.finding-item')).toHaveCount.greaterThan(0)
    
    // Check risk score is displayed
    await expect(page.locator('.risk-score')).toBeVisible()
  })

  test('should handle file upload errors', async ({ page }) => {
    await page.goto('http://localhost:3000')
    
    // Try to analyze without file
    await page.click('button:has-text("Analyze")')
    
    // Should show error or remain on upload screen
    await expect(page.locator('.upload-card')).toBeVisible()
  })

  test('should toggle dark mode', async ({ page }) => {
    await page.goto('http://localhost:3000')
    
    // Click theme toggle
    await page.click('.theme-toggle')
    
    // Check dark mode is applied
    await expect(page.locator('#app')).toHaveClass(/dark-mode/)
  })
})