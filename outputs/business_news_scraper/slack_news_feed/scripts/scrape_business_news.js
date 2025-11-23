const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const OUTPUT_DIR = '/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/slack_news_feed';
const SCREENSHOT_DIR = path.join(OUTPUT_DIR, 'screenshots');
const RAW_DIR = path.join(OUTPUT_DIR, 'raw');

async function scrapeWSJ(page) {
    console.log('Scraping Wall Street Journal...');
    await page.goto('https://www.wsj.com', { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(3000);

    // Take screenshot
    await page.screenshot({
        path: path.join(SCREENSHOT_DIR, 'wsj_homepage.png'),
        fullPage: true
    });

    // Extract headlines
    const headlines = await page.evaluate(() => {
        const results = [];

        // WSJ headline selectors
        const selectors = [
            'article h2',
            'article h3',
            '.WSJTheme--headline--7VCzo7Ay',
            '[data-id="article"] h2',
            '[data-id="article"] h3',
            'h2.WSJTheme--headline--unZqjb45',
            'h3.WSJTheme--headline--unZqjb45'
        ];

        const seen = new Set();

        for (const selector of selectors) {
            const elements = document.querySelectorAll(selector);
            elements.forEach(el => {
                const headline = el.textContent.trim();
                const article = el.closest('article') || el.closest('a') || el.parentElement;
                let url = '';
                let date = '';

                if (article) {
                    const link = article.querySelector('a') || (article.tagName === 'A' ? article : null);
                    if (link && link.href) {
                        url = link.href;
                    }

                    const timeEl = article.querySelector('time') || article.querySelector('[data-type="timestamp"]');
                    if (timeEl) {
                        date = timeEl.textContent.trim() || timeEl.getAttribute('datetime') || '';
                    }
                }

                if (headline && headline.length > 20 && headline.length < 300 && !seen.has(headline)) {
                    seen.add(headline);
                    results.push({ headline, date, url, summary: '' });
                }
            });
        }

        return results.slice(0, 20);
    });

    return headlines;
}

async function scrapeBusinessInsider(page) {
    console.log('Scraping Business Insider...');
    await page.goto('https://www.businessinsider.com', { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(3000);

    // Take screenshot
    await page.screenshot({
        path: path.join(SCREENSHOT_DIR, 'business_insider_homepage.png'),
        fullPage: true
    });

    // Extract headlines
    const headlines = await page.evaluate(() => {
        const results = [];

        // Business Insider selectors
        const selectors = [
            'h2[data-e2e-name="tout-title"]',
            'h3[data-e2e-name="tout-title"]',
            '.tout-title-link',
            'article h2',
            'article h3',
            '[data-testid="post-title"]'
        ];

        const seen = new Set();

        for (const selector of selectors) {
            const elements = document.querySelectorAll(selector);
            elements.forEach(el => {
                const headline = el.textContent.trim();
                const article = el.closest('article') || el.closest('[data-e2e-name="tout"]') || el.closest('a');
                let url = '';
                let date = '';

                if (article) {
                    const link = article.querySelector('a') || (article.tagName === 'A' ? article : null);
                    if (link && link.href) {
                        url = link.href;
                    }

                    const timeEl = article.querySelector('time') || article.querySelector('[data-e2e-name="byline-timestamp"]');
                    if (timeEl) {
                        date = timeEl.textContent.trim() || timeEl.getAttribute('datetime') || '';
                    }
                }

                if (headline && headline.length > 20 && headline.length < 300 && !seen.has(headline)) {
                    seen.add(headline);
                    results.push({ headline, date, url, summary: '' });
                }
            });
        }

        return results.slice(0, 20);
    });

    return headlines;
}

async function scrapeForbes(page) {
    console.log('Scraping Forbes...');
    await page.goto('https://www.forbes.com', { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(3000);

    // Take screenshot
    await page.screenshot({
        path: path.join(SCREENSHOT_DIR, 'forbes_homepage.png'),
        fullPage: true
    });

    // Extract headlines
    const headlines = await page.evaluate(() => {
        const results = [];

        // Forbes selectors
        const selectors = [
            'article h3',
            'article h2',
            '.stream-item__title',
            '[data-testid="article-title"]',
            '.card-title'
        ];

        const seen = new Set();

        for (const selector of selectors) {
            const elements = document.querySelectorAll(selector);
            elements.forEach(el => {
                const headline = el.textContent.trim();
                const article = el.closest('article') || el.closest('.stream-item') || el.closest('a');
                let url = '';
                let date = '';

                if (article) {
                    const link = article.querySelector('a') || (article.tagName === 'A' ? article : null);
                    if (link && link.href) {
                        url = link.href;
                    }

                    const timeEl = article.querySelector('time') || article.querySelector('.stream-item__date');
                    if (timeEl) {
                        date = timeEl.textContent.trim() || timeEl.getAttribute('datetime') || '';
                    }
                }

                if (headline && headline.length > 20 && headline.length < 300 && !seen.has(headline)) {
                    seen.add(headline);
                    results.push({ headline, date, url, summary: '' });
                }
            });
        }

        return results.slice(0, 20);
    });

    return headlines;
}

async function main() {
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
        userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    });
    const page = await context.newPage();

    const results = {
        timestamp: new Date().toISOString(),
        sources: {}
    };

    try {
        // Scrape WSJ
        results.sources.wsj = await scrapeWSJ(page);
        console.log(`Extracted ${results.sources.wsj.length} headlines from WSJ`);

        // Scrape Business Insider
        results.sources.businessInsider = await scrapeBusinessInsider(page);
        console.log(`Extracted ${results.sources.businessInsider.length} headlines from Business Insider`);

        // Scrape Forbes
        results.sources.forbes = await scrapeForbes(page);
        console.log(`Extracted ${results.sources.forbes.length} headlines from Forbes`);

        // Save raw data
        fs.writeFileSync(
            path.join(RAW_DIR, 'business_news_headlines.json'),
            JSON.stringify(results, null, 2)
        );

        console.log('Scraping completed successfully!');
        console.log(`Total headlines: ${results.sources.wsj.length + results.sources.businessInsider.length + results.sources.forbes.length}`);

    } catch (error) {
        console.error('Error during scraping:', error);
    } finally {
        await browser.close();
    }
}

main();
