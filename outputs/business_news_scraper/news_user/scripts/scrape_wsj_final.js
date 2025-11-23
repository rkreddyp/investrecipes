const { chromium } = require('playwright');
const fs = require('fs');

async function scrapeWSJViaGoogle(page) {
    console.log('Searching for WSJ articles via Google News...');

    try {
        await page.goto('https://news.google.com/search?q=site:wsj.com+business+when:1d&hl=en-US&gl=US&ceid=US:en', {
            waitUntil: 'domcontentloaded',
            timeout: 60000
        });

        await page.waitForTimeout(3000);

        await page.screenshot({
            path: '/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/news_user/screenshots/google_news_wsj_final.png',
            fullPage: true
        });

        const headlines = await page.evaluate(() => {
            const results = [];
            const seen = new Set();

            // Get all article-like containers
            const allLinks = Array.from(document.querySelectorAll('a'));

            for (let link of allLinks) {
                if (results.length >= 15) break;

                const text = link.innerText?.trim();
                let href = link.href;

                // Look for text that seems like headlines
                if (text &&
                    text.length > 25 &&
                    text.length < 250 &&
                    !seen.has(text) &&
                    !text.includes('©') &&
                    !text.includes('Google') &&
                    !text.match(/^\d+\s*(hour|minute|day)s?\s*ago$/i)) {

                    // Clean up Google News redirect URLs
                    if (href.includes('google.com')) {
                        // Try to extract actual URL from redirect
                        const match = href.match(/url=([^&]+)/);
                        if (match) {
                            href = decodeURIComponent(match[1]);
                        }
                    }

                    results.push({
                        headline: text,
                        url: href.includes('wsj.com') ? href : `https://www.wsj.com (article link via Google News)`,
                        time: 'Last 24 hours'
                    });
                    seen.add(text);
                }
            }

            return results;
        });

        console.log(`Found ${headlines.length} WSJ headlines via Google News`);
        return headlines.slice(0, 10);

    } catch (error) {
        console.error('Error scraping via Google News:', error.message);
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
        const headlines = await scrapeWSJViaGoogle(page);

        console.log('\n\n=== WSJ HEADLINES ===');
        console.log(`Total: ${headlines.length}\n`);

        headlines.forEach((h, idx) => {
            console.log(`${idx + 1}. ${h.headline}`);
        });

        if (headlines.length > 0) {
            fs.writeFileSync(
                '/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/news_user/raw/wsj_headlines.json',
                JSON.stringify(headlines, null, 2)
            );
            console.log('\n✓ Saved to wsj_headlines.json');
        }

    } catch (error) {
        console.error('Error:', error);
    } finally {
        await browser.close();
    }
}

main();
