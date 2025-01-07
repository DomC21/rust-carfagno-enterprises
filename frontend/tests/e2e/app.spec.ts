import { test, expect } from '@playwright/test';

test.describe('Rust: A Tool by Carfagno Enterprises', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('verify branding and UI elements', async ({ page }) => {
    await expect(page.getByTestId('header-title')).toContainText('Rust: A Tool by Carfagno Enterprises');
    await expect(page.getByTestId('stock-input')).toBeVisible();
    await expect(page.getByTestId('analyze-button')).toBeVisible();
  });

  test('test stock analysis workflow', async ({ page }) => {
    await page.getByTestId('stock-input').fill('AAPL');
    await page.getByTestId('analyze-button').click();
    await expect(page.getByTestId('analysis-results')).toBeVisible({ timeout: 30000 });
    await expect(page.getByTestId('sentiment-score')).toBeVisible();
    await expect(page.getByTestId('sentiment-chart')).toBeVisible();
    await expect(page.getByTestId('export-pdf')).toBeVisible();
    await expect(page.getByTestId('export-csv')).toBeVisible();
  });

  test('verify filter functionality', async ({ page }) => {
    await page.getByTestId('stock-input').fill('AAPL');
    await page.getByTestId('analyze-button').click();
    await expect(page.getByTestId('date-filter')).toBeVisible();
    await expect(page.getByTestId('publisher-filter')).toBeVisible();
    await expect(page.getByTestId('sentiment-filter')).toBeVisible();
  });

  test('test multi-ticker analysis', async ({ page }) => {
    const tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META'];
    for (const ticker of tickers) {
      await page.getByTestId('stock-input').fill(ticker);
      await page.getByTestId('analyze-button').click();
      await expect(page.getByTestId('analysis-results')).toBeVisible({ timeout: 30000 });
      await expect(page.getByTestId(`ticker-${ticker}`)).toBeVisible();
    }
  });

  test('verify export functionality', async ({ page }) => {
    await page.getByTestId('stock-input').fill('AAPL');
    await page.getByTestId('analyze-button').click();
    await expect(page.getByTestId('analysis-results')).toBeVisible({ timeout: 30000 });
    
    const pdfPromise = page.waitForEvent('download');
    await page.getByTestId('export-pdf').click();
    await pdfPromise;
    
    const csvPromise = page.waitForEvent('download');
    await page.getByTestId('export-csv').click();
    await csvPromise;
  });

  test('verify performance with high-volume queries', async ({ page }) => {
    const startTime = Date.now();
    const tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META'];
    
    for (const ticker of tickers) {
      await page.getByTestId('stock-input').fill(ticker);
      await page.getByTestId('analyze-button').click();
      await expect(page.getByTestId('analysis-results')).toBeVisible({ timeout: 30000 });
    }
    
    const endTime = Date.now();
    const totalTime = endTime - startTime;
    expect(totalTime).toBeLessThan(180000); // Should complete within 3 minutes
  });
});
