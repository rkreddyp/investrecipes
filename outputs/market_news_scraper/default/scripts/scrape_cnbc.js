const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  try {
    console.log('Navigating to CNBC...');
    await page.goto('https://www.cnbc.com', { waitUntil: 'networkidle', timeout: 60000 });

    // Take screenshot
    await page.screenshot({
      path: '/Users/venkat/workfolder/playwright-min/outputs/market_news_scraper/default/screenshots/cnbc_homepage.png',
      fullPage: true
    });
    console.log('Screenshot saved');

    // Extract headlines
    const headlines = await page.evaluate(() => {
      const results = [];

      // CNBC uses various selectors for headlines
      const selectors = [
        'a.Card-title',
        'a.LatestNews-headline',
        'a.RiverHeadline-headline',
        'a[data-test="headline-link"]',
        '.Card-standardBreakerCard a.Card-title',
        '.LatestNews-item a.LatestNews-headline'
      ];

      const links = new Set();

      selectors.forEach(selector => {
        const elements = document.querySelectorAll(selector);
        elements.forEach(el => {
          const text = el.textContent.trim();
          const url = el.href;
          if (text && url && !links.has(url)) {
            links.add(url);
            results.push({ headline: text, url: url });
          }
        });
      });

      return results.slice(0, 10);
    });

    console.log(JSON.stringify(headlines, null, 2));

  } catch (error) {
    console.error('Error:', error.message);
  } finally {
    await browser.close();
  }
})();
