const { chromium } = require('playwright');

async function scrapeBusinessInsider() {
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
        userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    });
    const page = await context.newPage();

    try {
        await page.goto('https://www.businessinsider.com', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(2000);

        const headlines = await page.evaluate(() => {
            const items = [];

            // Try multiple selectors for Business Insider articles
            const articleSelectors = [
                'article h2 a',
                'article h3 a',
                '.tout-title-link',
                '[data-testid="post-title"] a',
                'a[data-analytics-post-type="story"]',
                '.headline a',
                '.river-post__title a'
            ];

            const seenHeadlines = new Set();

            for (const selector of articleSelectors) {
                const elements = document.querySelectorAll(selector);
                elements.forEach(el => {
                    const headline = el.textContent?.trim();
                    const url = el.href;
                    if (headline && url && !seenHeadlines.has(headline) && headline.length > 10) {
                        seenHeadlines.add(headline);
                        items.push({
                            headline: headline,
                            url: url,
                            source: 'Business Insider'
                        });
                    }
                });
            }

            return items.slice(0, 20);
        });

        await browser.close();
        return headlines;
    } catch (error) {
        await browser.close();
        return { error: error.message };
    }
}

async function scrapeForbes() {
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
        userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    });
    const page = await context.newPage();

    try {
        await page.goto('https://www.forbes.com', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(2000);

        const headlines = await page.evaluate(() => {
            const items = [];

            // Try multiple selectors for Forbes articles
            const articleSelectors = [
                'article h3 a',
                'article h2 a',
                '.stream-item__title a',
                '[data-ga-track="Article"] a',
                '.article-headline a',
                'a[data-ga-track="recirc"]'
            ];

            const seenHeadlines = new Set();

            for (const selector of articleSelectors) {
                const elements = document.querySelectorAll(selector);
                elements.forEach(el => {
                    const headline = el.textContent?.trim();
                    const url = el.href;
                    if (headline && url && !seenHeadlines.has(headline) && headline.length > 10) {
                        seenHeadlines.add(headline);
                        items.push({
                            headline: headline,
                            url: url,
                            source: 'Forbes'
                        });
                    }
                });
            }

            return items.slice(0, 20);
        });

        await browser.close();
        return headlines;
    } catch (error) {
        await browser.close();
        return { error: error.message };
    }
}

async function scrapeWSJ() {
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
        userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    });
    const page = await context.newPage();

    try {
        await page.goto('https://www.wsj.com', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(2000);

        const headlines = await page.evaluate(() => {
            const items = [];

            // Try multiple selectors for WSJ articles
            const articleSelectors = [
                'article h2 a',
                'article h3 a',
                '.WSJTheme--headline--unZqjb45 a',
                '[data-module-zone="lead_positions"] h3 a',
                '.headline-link'
            ];

            const seenHeadlines = new Set();

            for (const selector of articleSelectors) {
                const elements = document.querySelectorAll(selector);
                elements.forEach(el => {
                    const headline = el.textContent?.trim();
                    const url = el.href;
                    if (headline && url && !seenHeadlines.has(headline) && headline.length > 10) {
                        seenHeadlines.add(headline);
                        items.push({
                            headline: headline,
                            url: url,
                            source: 'Wall Street Journal'
                        });
                    }
                });
            }

            return items.slice(0, 20);
        });

        await browser.close();
        return headlines;
    } catch (error) {
        await browser.close();
        return { error: error.message };
    }
}

async function main() {
    console.log('Starting business news scraping...\n');

    console.log('Scraping Business Insider...');
    const biHeadlines = await scrapeBusinessInsider();
    console.log(JSON.stringify({ businessInsider: biHeadlines }, null, 2));

    console.log('\nScraping Forbes...');
    const forbesHeadlines = await scrapeForbes();
    console.log(JSON.stringify({ forbes: forbesHeadlines }, null, 2));

    console.log('\nScraping Wall Street Journal...');
    const wsjHeadlines = await scrapeWSJ();
    console.log(JSON.stringify({ wsj: wsjHeadlines }, null, 2));
}

main();
