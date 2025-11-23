const { chromium } = require('playwright');
const fs = require('fs');

async function scrapeWSJViaGoogle(page) {
    console.log('Searching for WSJ articles via Google News...');

    try {
        // Use Google News to find recent WSJ business articles
        await page.goto('https://news.google.com/search?q=site:wsj.com+business+when:1d&hl=en-US&gl=US&ceid=US:en', {
            waitUntil: 'domcontentloaded',
            timeout: 60000
        });

        await page.waitForTimeout(3000);

        await page.screenshot({
            path: '/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/news_user/screenshots/google_news_wsj.png',
            fullPage: true
        });

        const headlines = await page.evaluate(() => {
            const results = [];
            const seen = new Set();

            // Google News article selectors
            const articles = document.querySelectorAll('article, [class*="article"]');

            for (let article of articles) {
                if (results.length >= 15) break;

                const headlineEl = article.querySelector('h3, h4, a');
                if (!headlineEl) continue;

                const text = headlineEl.innerText?.trim();
                const link = article.querySelector('a');

                if (text &&
                    text.length > 20 &&
                    text.length < 250 &&
                    !seen.has(text) &&
                    link) {

                    // Try to extract time
                    const timeEl = article.querySelector('time, [class*="time"], [class*="date"]');
                    const time = timeEl?.innerText || 'Recent';

                    results.push({
                        headline: text,
                        url: link.href,
                        time: time,
                        source: 'WSJ (via Google News)'
                    });
                    seen.add(text);
                }
            }

            return results;
        });

        console.log(`Found ${headlines.length} WSJ headlines via Google News`);
        return headlines;

    } catch (error) {
        console.error('Error scraping via Google News:', error.message);
        return [];
    }
}

async function scrapeMarketWatch(page) {
    console.log('\nTrying MarketWatch (WSJ sister site)...');

    try {
        await page.goto('https://www.marketwatch.com/latest-news', {
            waitUntil: 'domcontentloaded',
            timeout: 60000
        });

        await page.waitForTimeout(3000);

        await page.screenshot({
            path: '/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/news_user/screenshots/marketwatch.png',
            fullPage: true
        });

        const headlines = await page.evaluate(() => {
            const results = [];
            const seen = new Set();

            const allLinks = Array.from(document.querySelectorAll('a'));

            for (let link of allLinks) {
                if (results.length >= 15) break;

                const text = link.innerText?.trim();
                const href = link.href;

                if (text &&
                    text.length > 30 &&
                    text.length < 250 &&
                    !seen.has(text) &&
                    href &&
                    href.includes('marketwatch.com/story') &&
                    !text.includes('Subscribe') &&
                    !text.includes('©')) {

                    const timeEl = link.parentElement?.querySelector('time, [class*="time"]') ||
                                 link.closest('article')?.querySelector('time');
                    const time = timeEl?.innerText || 'Recent';

                    results.push({
                        headline: text,
                        url: href,
                        time: time,
                        source: 'MarketWatch'
                    });
                    seen.add(text);
                }
            }

            return results;
        });

        console.log(`Found ${headlines.length} MarketWatch headlines`);
        return headlines.slice(0, 10);

    } catch (error) {
        console.error('Error scraping MarketWatch:', error.message);
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

    try {
        const googleHeadlines = await scrapeWSJViaGoogle(page);
        const marketwatchHeadlines = await scrapeMarketWatch(page);

        const allHeadlines = [...googleHeadlines, ...marketwatchHeadlines];

        console.log('\n\n=== RESULTS ===');
        console.log(`Total headlines found: ${allHeadlines.length}`);

        if (allHeadlines.length > 0) {
            // Save to JSON
            fs.writeFileSync(
                '/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/news_user/raw/wsj_alternative_headlines.json',
                JSON.stringify(allHeadlines.slice(0, 10), null, 2)
            );
            console.log('\nSaved to: wsj_alternative_headlines.json');
        }

    } catch (error) {
        console.error('Error:', error);
    } finally {
        await browser.close();
    }
}

main();
