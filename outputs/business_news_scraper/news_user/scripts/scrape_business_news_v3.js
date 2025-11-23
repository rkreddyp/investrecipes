const { chromium } = require('playwright');
const fs = require('fs');

async function scrapeWSJ(page) {
    console.log('Navigating to WSJ...');

    try {
        // Try the RSS feed or text version
        await page.goto('https://www.wsj.com/news/business', { waitUntil: 'domcontentloaded', timeout: 60000 });
        await page.waitForTimeout(5000);

        await page.screenshot({
            path: '/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/news_user/screenshots/wsj_business.png',
            fullPage: true
        });

        const headlines = await page.evaluate(() => {
            const results = [];
            const seen = new Set();

            // Get all links
            const allLinks = Array.from(document.querySelectorAll('a'));

            for (let link of allLinks) {
                if (results.length >= 20) break;

                const text = link.innerText?.trim();
                const href = link.href;

                // Filter for article headlines
                if (text &&
                    text.length > 30 &&
                    text.length < 250 &&
                    !seen.has(text) &&
                    href &&
                    href.includes('/articles/') &&
                    !text.includes('Subscribe') &&
                    !text.includes('Sign In') &&
                    !text.includes('©')) {

                    // Look for time element nearby
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

        console.log(`Found ${headlines.length} WSJ headlines`);
        return headlines.slice(0, 10);
    } catch (error) {
        console.error('Error scraping WSJ:', error.message);
        return [];
    }
}

async function scrapeBusinessInsider(page) {
    console.log('Navigating to Business Insider...');

    try {
        await page.goto('https://www.businessinsider.com/latest', { waitUntil: 'domcontentloaded', timeout: 60000 });
        await page.waitForTimeout(5000);

        await page.screenshot({
            path: '/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/news_user/screenshots/businessinsider_latest.png',
            fullPage: true
        });

        const headlines = await page.evaluate(() => {
            const results = [];
            const seen = new Set();

            const allLinks = Array.from(document.querySelectorAll('a'));

            for (let link of allLinks) {
                if (results.length >= 20) break;

                const text = link.innerText?.trim();
                const href = link.href;

                if (text &&
                    text.length > 30 &&
                    text.length < 300 &&
                    !seen.has(text) &&
                    href &&
                    href.includes('businessinsider.com/') &&
                    !text.includes('Subscribe') &&
                    !text.includes('Menu') &&
                    !text.includes('©')) {

                    const timeEl = link.closest('article')?.querySelector('time') ||
                                 link.parentElement?.querySelector('time');
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

        console.log(`Found ${headlines.length} Business Insider headlines`);
        return headlines.slice(0, 10);
    } catch (error) {
        console.error('Error scraping Business Insider:', error.message);
        return [];
    }
}

async function scrapeForbes(page) {
    console.log('Navigating to Forbes...');

    try {
        await page.goto('https://www.forbes.com/business/', { waitUntil: 'domcontentloaded', timeout: 60000 });
        await page.waitForTimeout(5000);

        await page.screenshot({
            path: '/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/news_user/screenshots/forbes_business.png',
            fullPage: true
        });

        const headlines = await page.evaluate(() => {
            const results = [];
            const seen = new Set();

            // Get all links
            const allLinks = Array.from(document.querySelectorAll('a'));

            for (let link of allLinks) {
                if (results.length >= 20) break;

                const text = link.innerText?.trim();
                const href = link.href;

                // Filter for Forbes article headlines
                if (text &&
                    text.length > 30 &&
                    text.length < 300 &&
                    !seen.has(text) &&
                    href &&
                    (href.includes('/sites/') || href.includes('forbes.com/')) &&
                    !text.includes('Subscribe') &&
                    !text.includes('Sign In') &&
                    !text.includes('Forbes') &&
                    !text.includes('©')) {

                    // Look for time/date nearby
                    const timeEl = link.closest('article')?.querySelector('time') ||
                                 link.parentElement?.querySelector('[class*="date"]') ||
                                 link.parentElement?.querySelector('time');
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

        console.log(`Found ${headlines.length} Forbes headlines`);
        return headlines.slice(0, 10);
    } catch (error) {
        console.error('Error scraping Forbes:', error.message);
        return [];
    }
}

function formatMarkdown(wsjHeadlines, biHeadlines, forbesHeadlines) {
    let markdown = '## Business News Sources\n\n';

    markdown += '### Wall Street Journal\n';
    if (wsjHeadlines.length > 0) {
        wsjHeadlines.forEach((item, idx) => {
            markdown += `${idx + 1}. **${item.time}** - ${item.headline}\n`;
            markdown += `   - URL: ${item.url}\n\n`;
        });
    } else {
        markdown += '*No headlines could be extracted (site requires verification)*\n\n';
    }

    markdown += '### Business Insider\n';
    if (biHeadlines.length > 0) {
        biHeadlines.forEach((item, idx) => {
            markdown += `${idx + 1}. **${item.time}** - ${item.headline}\n`;
            markdown += `   - URL: ${item.url}\n\n`;
        });
    } else {
        markdown += '*No headlines could be extracted*\n\n';
    }

    markdown += '### Forbes\n';
    if (forbesHeadlines.length > 0) {
        forbesHeadlines.forEach((item, idx) => {
            markdown += `${idx + 1}. **${item.time}** - ${item.headline}\n`;
            markdown += `   - URL: ${item.url}\n\n`;
        });
    } else {
        markdown += '*No headlines could be extracted*\n\n';
    }

    return markdown;
}

async function main() {
    const browser = await chromium.launch({
        headless: true,
        args: ['--disable-blink-features=AutomationControlled']
    });

    const context = await browser.newContext({
        userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        viewport: { width: 1920, height: 1080 },
        extraHTTPHeaders: {
            'Accept-Language': 'en-US,en;q=0.9'
        }
    });

    const page = await context.newPage();

    try {
        const biHeadlines = await scrapeBusinessInsider(page);
        const forbesHeadlines = await scrapeForbes(page);
        const wsjHeadlines = await scrapeWSJ(page);

        const markdown = formatMarkdown(wsjHeadlines, biHeadlines, forbesHeadlines);

        const reportPath = '/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/news_user/reports/business_news_headlines_20251117.md';
        fs.writeFileSync(reportPath, markdown);

        console.log(`\nReport saved to: ${reportPath}`);
        console.log('\nSummary:');
        console.log(`- WSJ: ${wsjHeadlines.length} headlines`);
        console.log(`- Business Insider: ${biHeadlines.length} headlines`);
        console.log(`- Forbes: ${forbesHeadlines.length} headlines`);

    } catch (error) {
        console.error('Error during scraping:', error);
    } finally {
        await browser.close();
    }
}

main();
