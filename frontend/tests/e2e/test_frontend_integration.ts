import { test, expect } from '@playwright/test';

test.describe('Rust: A Tool by Carfagno Enterprises - Frontend Integration Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('https://rust-carfagno-enterprises-3.onrender.com');
  });

  test('verify branding and UI elements', async ({ page }) => {
    // Check header branding
    await expect(page.locator('h1')).toContainText('Rust: A Tool by Carfagno Enterprises');
    
    // Verify stock input functionality
    const stockInput = page.locator('[data-testid="stock-input"]');
    await expect(stockInput).toBeVisible();
    
    // Verify filters presence
    const dateFilter = page.locator('[data-testid="date-filter"]');
    const publisherFilter = page.locator('[data-testid="publisher-filter"]');
    const sentimentFilter = page.locator('[data-testid="sentiment-filter"]');
    await expect(dateFilter).toBeVisible();
    await expect(publisherFilter).toBeVisible();
    await expect(sentimentFilter).toBeVisible();
  });

  test('test stock analysis workflow', async ({ page }) => {
    // Input stock ticker
    await page.fill('[data-testid="stock-input"]', 'AAPL');
    await page.click('[data-testid="analyze-button"]');
    
    // Wait for analysis results
    await expect(page.locator('[data-testid="analysis-results"]')).toBeVisible({ timeout: 30000 });
    
    // Verify sentiment indicators
    const sentimentScore = page.locator('[data-testid="sentiment-score"]');
    await expect(sentimentScore).toBeVisible();
    
    // Check for article summaries
    const articleSummaries = page.locator('[data-testid="article-summary"]');
    const count = await articleSummaries.count();
    expect(count).toBeGreaterThan(0);
  });

  test('verify export functionality', async ({ page }) => {
    // Input stock and get analysis
    await page.fill('[data-testid="stock-input"]', 'MSFT');
    await page.click('[data-testid="analyze-button"]');
    await expect(page.locator('[data-testid="analysis-results"]')).toBeVisible({ timeout: 30000 });
    
    // Test PDF export
    const pdfButton = page.locator('[data-testid="export-pdf"]');
    await expect(pdfButton).toBeVisible();
    const pdfDownload = page.waitForEvent('download');
    await pdfButton.click();
    const pdf = await pdfDownload;
    expect(pdf.suggestedFilename()).toContain('.pdf');
    
    // Test CSV export
    const csvButton = page.locator('[data-testid="export-csv"]');
    await expect(csvButton).toBeVisible();
    const csvDownload = page.waitForEvent('download');
    await csvButton.click();
    const csv = await csvDownload;
    expect(csv.suggestedFilename()).toContain('.csv');
  });

  test('verify performance with multiple tickers', async ({ page }) => {
    const tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META'];
    
    for (const ticker of tickers) {
      // Input stock ticker
      await page.fill('[data-testid="stock-input"]', ticker);
      await page.click('[data-testid="analyze-button"]');
      
      // Verify quick response
      await expect(page.locator('[data-testid="analysis-results"]')).toBeVisible({ 
        timeout: 30000 
      });
      
      // Clear results for next ticker
      await page.click('[data-testid="clear-button"]');
    }
  });
});
