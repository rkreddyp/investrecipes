const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
  });
  const page = await context.newPage();

  console.log('Scraping Forbes...');
  await page.goto('https://www.forbes.com', { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(3000);

  const headlines = await page.evaluate(() => {
    const results = [];
    const seenHeadlines = new Set();

    // Try multiple selectors for articles
    const articleSelectors = [
      'article h3 a',
      'article h2 a',
      '.stream-item__title a',
      '[data-ga-track="Hero"] h1 a',
      '[data-ga-track="Hero"] h2 a',
      '.card-title a',
      'h3 a',
      'h2 a'
    ];

    for (const selector of articleSelectors) {
      const elements = document.querySelectorAll(selector);
      elements.forEach(el => {
        const headline = el.textContent.trim();
        const url = el.href;

        if (headline && headline.length > 10 && !seenHeadlines.has(headline) && url) {
          seenHeadlines.add(headline);

          // Try to find date/time
          let dateText = '';
          let parent = el.closest('article') || el.closest('div[class*="stream"]') || el.closest('div[class*="card"]');
          if (parent) {
            const timeEl = parent.querySelector('time') || parent.querySelector('[class*="timestamp"]') || parent.querySelector('[class*="date"]');
            if (timeEl) {
              dateText = timeEl.textContent.trim() || timeEl.getAttribute('datetime') || '';
            }
          }

          results.push({
            headline: headline,
            date: dateText,
            url: url,
            summary: ''
          });
        }
      });

      if (results.length >= 20) break;
    }

    return results.slice(0, 20);
  });

  fs.writeFileSync(
    '/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/default/raw/forbes.json',
    JSON.stringify(headlines, null, 2)
  );
  console.log(`Found ${headlines.length} headlines`);

  await browser.close();
})();
