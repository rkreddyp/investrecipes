const { chromium } = require('playwright');

async function scrapeForbes() {
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
        userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    });
    const page = await context.newPage();

    try {
        await page.goto('https://www.forbes.com', { waitUntil: 'domcontentloaded', timeout: 30000 });
        await page.waitForTimeout(3000);

        const headlines = await page.evaluate(() => {
            const items = [];
            const seenHeadlines = new Set();

            // Get all anchor tags
            const allLinks = document.querySelectorAll('a');

            allLinks.forEach(link => {
                const text = link.textContent?.trim();
                const href = link.href;

                // Filter for article links - they typically contain /sites/ or article paths
                if (text && href &&
                    text.length > 20 &&
                    text.length < 200 &&
                    !seenHeadlines.has(text) &&
                    (href.includes('forbes.com/sites/') ||
                     href.includes('forbes.com/') && text.match(/[A-Z]/))) {

                    // Exclude navigation/menu items
                    const excludeTerms = ['Subscribe', 'Sign In', 'Forbes', 'Newsletter', 'Menu', 'Search'];
                    if (!excludeTerms.some(term => text.includes(term))) {
                        seenHeadlines.add(text);
                        items.push({
                            headline: text,
                            url: href,
                            source: 'Forbes'
                        });
                    }
                }
            });

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
        await page.goto('https://www.wsj.com', { waitUntil: 'domcontentloaded', timeout: 30000 });
        await page.waitForTimeout(3000);

        const headlines = await page.evaluate(() => {
            const items = [];
            const seenHeadlines = new Set();

            // Get all anchor tags within articles or headlines
            const allLinks = document.querySelectorAll('a');

            allLinks.forEach(link => {
                const text = link.textContent?.trim();
                const href = link.href;

                // Filter for article links
                if (text && href &&
                    text.length > 20 &&
                    text.length < 250 &&
                    !seenHeadlines.has(text) &&
                    href.includes('wsj.com/') &&
                    href.includes('articles/')) {

                    // Exclude navigation/menu items
                    const excludeTerms = ['Subscribe', 'Sign In', 'WSJ', 'Menu', 'Print Edition', 'Log In'];
                    if (!excludeTerms.some(term => text.includes(term))) {
                        seenHeadlines.add(text);
                        items.push({
                            headline: text,
                            url: href,
                            source: 'Wall Street Journal'
                        });
                    }
                }
            });

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
    console.log('Scraping Forbes...');
    const forbesHeadlines = await scrapeForbes();
    console.log(JSON.stringify({ forbes: forbesHeadlines }, null, 2));

    console.log('\nScraping Wall Street Journal...');
    const wsjHeadlines = await scrapeWSJ();
    console.log(JSON.stringify({ wsj: wsjHeadlines }, null, 2));
}

main();
