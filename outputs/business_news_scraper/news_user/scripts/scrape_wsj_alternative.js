const { chromium } = require('playwright');
const fs = require('fs');

async function scrapeWSJAlternatives(page) {
    const attempts = [
        {
            url: 'https://www.wsj.com/news/business?mod=nav_top_section',
            name: 'WSJ Business Section'
        },
        {
            url: 'https://www.wsj.com/news/types/journal-reports',
            name: 'WSJ Journal Reports'
        },
        {
            url: 'https://www.wsj.com/news/latest-headlines',
            name: 'WSJ Latest Headlines'
        }
    ];

    for (let attempt of attempts) {
        console.log(`\nTrying: ${attempt.name}`);
        console.log(`URL: ${attempt.url}`);

        try {
            await page.goto(attempt.url, { waitUntil: 'domcontentloaded', timeout: 60000 });
            await page.waitForTimeout(5000);

            const screenshotName = attempt.name.toLowerCase().replace(/\s+/g, '_');
            await page.screenshot({
                path: `/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/news_user/screenshots/${screenshotName}.png`,
                fullPage: true
            });

            // Check if captcha is present
            const hasCaptcha = await page.evaluate(() => {
                return document.body.innerText.includes('Verification Required');
            });

            if (hasCaptcha) {
                console.log('  ❌ Captcha detected');
                continue;
            }

            // Extract headlines
            const headlines = await page.evaluate(() => {
                const results = [];
                const seen = new Set();

                // Get all links
                const allLinks = Array.from(document.querySelectorAll('a'));

                for (let link of allLinks) {
                    if (results.length >= 20) break;

                    const text = link.innerText?.trim();
                    const href = link.href;

                    if (text &&
                        text.length > 30 &&
                        text.length < 250 &&
                        !seen.has(text) &&
                        href &&
                        href.includes('/articles/') &&
                        !text.includes('Subscribe') &&
                        !text.includes('Sign In') &&
                        !text.includes('©')) {

                        const timeEl = link.parentElement?.querySelector('time') ||
                                     link.closest('article')?.querySelector('time');
                        const time = timeEl?.innerText || 'Recent';

                        results.push({
                            headline: text,
                            url: href,
                            time: time
                        });
                        seen.add(text);
                    }
                }

                return results;
            });

            if (headlines.length > 0) {
                console.log(`  ✓ Found ${headlines.length} headlines`);
                return headlines.slice(0, 10);
            } else {
                console.log('  ❌ No headlines found');
            }

        } catch (error) {
            console.log(`  ❌ Error: ${error.message}`);
        }
    }

    return [];
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
        const headlines = await scrapeWSJAlternatives(page);

        console.log('\n\n=== RESULTS ===');
        console.log(`Total WSJ headlines found: ${headlines.length}`);

        if (headlines.length > 0) {
            console.log('\nHeadlines:');
            headlines.forEach((h, idx) => {
                console.log(`${idx + 1}. ${h.headline}`);
            });

            // Save to JSON for later use
            fs.writeFileSync(
                '/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/news_user/raw/wsj_headlines.json',
                JSON.stringify(headlines, null, 2)
            );
        }

    } catch (error) {
        console.error('Error:', error);
    } finally {
        await browser.close();
    }
}

main();
