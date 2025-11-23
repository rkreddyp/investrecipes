const { chromium } = require('playwright');

async function scrapeForbesNews() {
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
        userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    });
    const page = await context.newPage();

    try {
        // Try Forbes Money/Business section instead of homepage
        await page.goto('https://www.forbes.com/money/', { waitUntil: 'domcontentloaded', timeout: 30000 });
        await page.waitForTimeout(3000);

        const headlines = await page.evaluate(() => {
            const items = [];
            const seenHeadlines = new Set();

            // Get all anchor tags
            const allLinks = document.querySelectorAll('a');

            allLinks.forEach(link => {
                const text = link.textContent?.trim();
                const href = link.href;

                // Filter for article links
                if (text && href &&
                    text.length > 20 &&
                    text.length < 200 &&
                    !seenHeadlines.has(text) &&
                    href.includes('forbes.com/sites/')) {

                    // Exclude navigation/menu items and lists
                    const excludeTerms = [
                        'Subscribe', 'Sign In', 'Forbes', 'Newsletter', 'Menu', 'Search',
                        'Top Wealth', 'Best-In-State', 'Richest', 'Most Powerful',
                        'Next Billion-Dollar', 'Paid Program', 'America\'s'
                    ];
                    const hasExcludedTerm = excludeTerms.some(term => text.includes(term));

                    // Only include if it's a recent article (check if URL contains /2025/ or /2024/)
                    const isRecent = href.includes('/2025/11/') ||
                                    href.includes('/2025/10/') ||
                                    href.includes('/2024/12/');

                    if (!hasExcludedTerm && isRecent) {
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

async function scrapeForbesBreaking() {
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
        userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    });
    const page = await context.newPage();

    try {
        // Try Forbes Breaking News section
        await page.goto('https://www.forbes.com/breaking/', { waitUntil: 'domcontentloaded', timeout: 30000 });
        await page.waitForTimeout(3000);

        const headlines = await page.evaluate(() => {
            const items = [];
            const seenHeadlines = new Set();

            const allLinks = document.querySelectorAll('a');

            allLinks.forEach(link => {
                const text = link.textContent?.trim();
                const href = link.href;

                if (text && href &&
                    text.length > 20 &&
                    text.length < 200 &&
                    !seenHeadlines.has(text) &&
                    href.includes('forbes.com/sites/')) {

                    const excludeTerms = [
                        'Subscribe', 'Sign In', 'Forbes', 'Newsletter', 'Menu',
                        'Top Wealth', 'Best-In-State', 'Paid Program'
                    ];
                    const hasExcludedTerm = excludeTerms.some(term => text.includes(term));

                    if (!hasExcludedTerm) {
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

async function main() {
    console.log('Scraping Forbes Money section...');
    const forbesMoney = await scrapeForbesNews();
    console.log(JSON.stringify({ forbesMoney: forbesMoney }, null, 2));

    console.log('\nScraping Forbes Breaking News...');
    const forbesBreaking = await scrapeForbesBreaking();
    console.log(JSON.stringify({ forbesBreaking: forbesBreaking }, null, 2));
}

main();
