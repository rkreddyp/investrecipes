const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    viewport: { width: 1920, height: 1080 },
    extraHTTPHeaders: {
      'Accept-Language': 'en-US,en;q=0.9',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
  });
  const page = await context.newPage();

  console.log('Scraping Wall Street Journal...');

  try {
    await page.goto('https://www.wsj.com', { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(5000);

    // Take updated screenshot
    await page.screenshot({
      path: '/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/default/screenshots/wsj_homepage_retry.png',
      fullPage: true
    });

    const headlines = await page.evaluate(() => {
      const results = [];
      const seenHeadlines = new Set();

      // Try multiple selectors for WSJ articles
      const articleSelectors = [
        'article h3 a',
        'article h2 a',
        '[data-module-zone="lead_positions"] h3 a',
        '[data-module-zone="lead_positions"] h2 a',
        '.WSJTheme--headline a',
        'h3.WSJTheme--headline',
        'h2.WSJTheme--headline',
        '.css-xgokil a',
        '.css-6wv4vo a'
      ];

      for (const selector of articleSelectors) {
        const elements = document.querySelectorAll(selector);
        elements.forEach(el => {
          let headline = '';
          let url = '';

          if (el.tagName === 'A') {
            headline = el.textContent.trim();
            url = el.href;
          } else {
            const link = el.querySelector('a');
            headline = el.textContent.trim();
            url = link ? link.href : '';
          }

          if (headline && headline.length > 10 && !seenHeadlines.has(headline) && url) {
            seenHeadlines.add(headline);

            // Try to find date/time
            let dateText = '';
            let parent = el.closest('article') || el.closest('[data-module-zone]') || el.closest('div');
            if (parent) {
              const timeEl = parent.querySelector('time') || parent.querySelector('[class*="timestamp"]') || parent.querySelector('[class*="date"]');
              if (timeEl) {
                dateText = timeEl.textContent.trim() || timeEl.getAttribute('datetime') || '';
              }
            }

            results.push({
              headline: headline,
              date: dateText,
              url: url.startsWith('http') ? url : `https://www.wsj.com${url}`,
              summary: ''
            });
          }
        });

        if (results.length >= 20) break;
      }

      return results.slice(0, 20);
    });

    fs.writeFileSync(
      '/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/default/raw/wsj.json',
      JSON.stringify(headlines, null, 2)
    );
    console.log(`Found ${headlines.length} headlines`);

  } catch (error) {
    console.error('Error scraping WSJ:', error.message);
    // Save error info
    fs.writeFileSync(
      '/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/default/raw/wsj.json',
      JSON.stringify({ error: 'Access blocked or site unavailable', details: error.message }, null, 2)
    );
  }

  await browser.close();
})();
