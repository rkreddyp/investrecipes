const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function scrapeBloomberg(page) {
  console.log('Navigating to Bloomberg...');
  await page.goto('https://www.bloomberg.com', { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(3000);

  const screenshotPath = '/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/financial_news/screenshots/bloomberg.png';
  await page.screenshot({ path: screenshotPath, fullPage: true });
  console.log(`Screenshot saved: ${screenshotPath}`);

  // Extract headlines
  const headlines = await page.evaluate(() => {
    const results = [];
    const articles = document.querySelectorAll('article, [data-component="story"], .story-package-module__story');

    for (let i = 0; i < Math.min(articles.length, 20); i++) {
      const article = articles[i];
      const headlineEl = article.querySelector('a[href*="/news/"], a[href*="/articles/"], h3 a, h2 a, .headline a, [class*="headline"] a');

      if (headlineEl) {
        const headline = headlineEl.textContent.trim();
        let url = headlineEl.href;

        // Make URL absolute
        if (url && !url.startsWith('http')) {
          url = new URL(url, 'https://www.bloomberg.com').href;
        }

        if (headline && headline.length > 10) {
          results.push({
            headline: headline,
            url: url || '',
            date: ''
          });
        }
      }
    }

    return results;
  });

  return headlines.slice(0, 10);
}

async function scrapeReuters(page) {
  console.log('Navigating to Reuters Business...');
  await page.goto('https://www.reuters.com/business', { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(3000);

  const screenshotPath = '/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/financial_news/screenshots/reuters.png';
  await page.screenshot({ path: screenshotPath, fullPage: true });
  console.log(`Screenshot saved: ${screenshotPath}`);

  // Extract headlines
  const headlines = await page.evaluate(() => {
    const results = [];
    const articles = document.querySelectorAll('[data-testid="MediaStoryCard"], [data-testid="TextStoryCard"], article, li[class*="story"]');

    for (let i = 0; i < Math.min(articles.length, 20); i++) {
      const article = articles[i];
      const headlineEl = article.querySelector('a[data-testid="Heading"], a[data-testid="Link"], h3 a, h2 a, a[class*="Heading"]');

      if (headlineEl) {
        const headline = headlineEl.textContent.trim();
        let url = headlineEl.href;

        if (url && !url.startsWith('http')) {
          url = new URL(url, 'https://www.reuters.com').href;
        }

        const timeEl = article.querySelector('time, [data-testid="Label"]');
        const date = timeEl ? timeEl.textContent.trim() : '';

        if (headline && headline.length > 10) {
          results.push({
            headline: headline,
            url: url || '',
            date: date
          });
        }
      }
    }

    return results;
  });

  return headlines.slice(0, 10);
}

async function scrapeFT(page) {
  console.log('Navigating to Financial Times...');
  await page.goto('https://www.ft.com', { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(3000);

  const screenshotPath = '/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/financial_news/screenshots/ft.png';
  await page.screenshot({ path: screenshotPath, fullPage: true });
  console.log(`Screenshot saved: ${screenshotPath}`);

  // Extract headlines
  const headlines = await page.evaluate(() => {
    const results = [];
    const articles = document.querySelectorAll('[data-trackable="story-card"], article, .o-teaser, li[class*="story"]');

    for (let i = 0; i < Math.min(articles.length, 20); i++) {
      const article = articles[i];
      const headlineEl = article.querySelector('a[class*="headline"], a[data-trackable="heading-link"], h3 a, h2 a, .o-teaser__heading a');

      if (headlineEl) {
        const headline = headlineEl.textContent.trim();
        let url = headlineEl.href;

        if (url && !url.startsWith('http')) {
          url = new URL(url, 'https://www.ft.com').href;
        }

        const timeEl = article.querySelector('time, .o-teaser__timestamp');
        const date = timeEl ? timeEl.textContent.trim() : '';

        if (headline && headline.length > 10) {
          results.push({
            headline: headline,
            url: url || '',
            date: date
          });
        }
      }
    }

    return results;
  });

  return headlines.slice(0, 10);
}

async function main() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
  });
  const page = await context.newPage();

  const results = {
    bloomberg: [],
    reuters: [],
    ft: []
  };

  try {
    results.bloomberg = await scrapeBloomberg(page);
    console.log(`Bloomberg: ${results.bloomberg.length} headlines extracted`);
  } catch (error) {
    console.error('Bloomberg error:', error.message);
  }

  try {
    results.reuters = await scrapeReuters(page);
    console.log(`Reuters: ${results.reuters.length} headlines extracted`);
  } catch (error) {
    console.error('Reuters error:', error.message);
  }

  try {
    results.ft = await scrapeFT(page);
    console.log(`FT: ${results.ft.length} headlines extracted`);
  } catch (error) {
    console.error('FT error:', error.message);
  }

  await browser.close();

  // Save results
  const outputPath = '/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/financial_news/raw/headlines.json';
  fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
  console.log(`Results saved to: ${outputPath}`);

  return results;
}

main().catch(console.error);
