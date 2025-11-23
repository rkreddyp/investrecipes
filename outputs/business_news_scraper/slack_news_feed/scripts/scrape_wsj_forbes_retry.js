const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const OUTPUT_DIR = '/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/slack_news_feed';
const SCREENSHOT_DIR = path.join(OUTPUT_DIR, 'screenshots');
const RAW_DIR = path.join(OUTPUT_DIR, 'raw');

async function scrapeWSJAlternative(page) {
    console.log('Scraping Wall Street Journal (alternative approach)...');

    // Try different user agent and stealth techniques
    try {
        await page.goto('https://www.wsj.com/news/latest-headlines', { waitUntil: 'domcontentloaded', timeout: 20000 });
        await page.waitForTimeout(5000);

        // Take screenshot
        await page.screenshot({
            path: path.join(SCREENSHOT_DIR, 'wsj_latest_headlines.png'),
            fullPage: true
        });

        const headlines = await page.evaluate(() => {
            const results = [];
            const seen = new Set();

            // Try multiple selector strategies
            const articleElements = document.querySelectorAll('article, [class*="article"], [class*="story"]');

            articleElements.forEach(article => {
                const headlineEl = article.querySelector('h2, h3, h4, [class*="headline"], [class*="title"]');
                if (headlineEl) {
                    const headline = headlineEl.textContent.trim();
                    let url = '';
                    let date = '';

                    const link = article.querySelector('a') || headlineEl.querySelector('a');
                    if (link && link.href) {
                        url = link.href;
                    }

                    const timeEl = article.querySelector('time');
                    if (timeEl) {
                        date = timeEl.textContent.trim() || timeEl.getAttribute('datetime') || '';
                    }

                    if (headline && headline.length > 20 && headline.length < 300 && !seen.has(headline)) {
                        seen.add(headline);
                        results.push({ headline, date, url, summary: '' });
                    }
                }
            });

            return results.slice(0, 20);
        });

        return headlines;
    } catch (error) {
        console.error('WSJ scraping failed:', error.message);
        return [];
    }
}

async function scrapeForbesImproved(page) {
    console.log('Scraping Forbes (improved)...');

    try {
        await page.goto('https://www.forbes.com/business/', { waitUntil: 'domcontentloaded', timeout: 20000 });
        await page.waitForTimeout(5000);

        // Take screenshot
        await page.screenshot({
            path: path.join(SCREENSHOT_DIR, 'forbes_business.png'),
            fullPage: true
        });

        const headlines = await page.evaluate(() => {
            const results = [];
            const seen = new Set();

            // Multiple selector strategies
            const selectors = [
                'article',
                '[class*="stream-item"]',
                '[class*="card"]',
                '[data-ga-track="recirc"]'
            ];

            selectors.forEach(selector => {
                const elements = document.querySelectorAll(selector);
                elements.forEach(el => {
                    // Look for headline elements
                    const headlineEl = el.querySelector('h2, h3, h4, a[class*="title"], a[class*="headline"]');
                    if (headlineEl) {
                        const headline = headlineEl.textContent.trim();
                        let url = '';
                        let date = '';

                        const link = headlineEl.closest('a') || headlineEl.querySelector('a') || el.querySelector('a');
                        if (link && link.href) {
                            url = link.href;
                        }

                        const timeEl = el.querySelector('time, [class*="date"], [class*="time"]');
                        if (timeEl) {
                            date = timeEl.textContent.trim() || timeEl.getAttribute('datetime') || '';
                        }

                        if (headline && headline.length > 20 && headline.length < 300 && !seen.has(headline)) {
                            seen.add(headline);
                            results.push({ headline, date, url, summary: '' });
                        }
                    }
                });
            });

            return results.slice(0, 20);
        });

        return headlines;
    } catch (error) {
        console.error('Forbes scraping failed:', error.message);
        return [];
    }
}

async function main() {
    const browser = await chromium.launch({
        headless: true,
        args: ['--disable-blink-features=AutomationControlled']
    });

    const context = await browser.newContext({
        userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        viewport: { width: 1920, height: 1080 }
    });

    const page = await context.newPage();

    // Add stealth settings
    await page.addInitScript(() => {
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    });

    const results = {
        timestamp: new Date().toISOString(),
        sources: {}
    };

    try {
        // Scrape WSJ
        results.sources.wsj = await scrapeWSJAlternative(page);
        console.log(`Extracted ${results.sources.wsj.length} headlines from WSJ`);

        // Scrape Forbes
        results.sources.forbes = await scrapeForbesImproved(page);
        console.log(`Extracted ${results.sources.forbes.length} headlines from Forbes`);

        // Save raw data
        fs.writeFileSync(
            path.join(RAW_DIR, 'wsj_forbes_headlines.json'),
            JSON.stringify(results, null, 2)
        );

        console.log('Scraping completed!');
        console.log(`Total headlines: ${results.sources.wsj.length + results.sources.forbes.length}`);

    } catch (error) {
        console.error('Error during scraping:', error);
    } finally {
        await browser.close();
    }
}

main();
