const { chromium } = require('playwright');
const fs = require('fs');

async function scrapeWSJ(page) {
    console.log('Navigating to WSJ...');

    try {
        await page.goto('https://www.wsj.com/business', { waitUntil: 'domcontentloaded', timeout: 60000 });
        await page.waitForTimeout(5000);

        // Take screenshot
        await page.screenshot({
            path: '/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/news_user/screenshots/wsj_homepage.png',
            fullPage: true
        });

        // Extract headlines with more flexible selectors
        const headlines = await page.evaluate(() => {
            const results = [];
            const seen = new Set();

            // Try multiple selector strategies
            const selectors = [
                'article h2, article h3',
                '[class*="headline"]',
                '[class*="WSJTheme--headline"]',
                'a[href*="/articles/"]',
                '.article-item h3',
                '.headline'
            ];

            for (let selector of selectors) {
                const elements = document.querySelectorAll(selector);

                for (let el of elements) {
                    if (results.length >= 20) break;

                    let headline = el.innerText?.trim();
                    let link = el.closest('a') || el.querySelector('a');

                    if (!headline && el.tagName === 'A') {
                        headline = el.innerText?.trim();
                        link = el;
                    }

                    if (headline && link && headline.length > 15 && !seen.has(headline)) {
                        const url = link.href;
                        const timeEl = el.closest('article')?.querySelector('time') ||
                                     el.parentElement?.querySelector('time');
                        const time = timeEl?.getAttribute('datetime') || timeEl?.innerText || '';

                        results.push({
                            headline: headline.substring(0, 200),
                            url: url,
                            time: time
                        });
                        seen.add(headline);
                    }
                }

                if (results.length >= 10) break;
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
        await page.goto('https://www.businessinsider.com/', { waitUntil: 'domcontentloaded', timeout: 60000 });
        await page.waitForTimeout(5000);

        await page.screenshot({
            path: '/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/news_user/screenshots/businessinsider_homepage.png',
            fullPage: true
        });

        const headlines = await page.evaluate(() => {
            const results = [];
            const seen = new Set();

            // Look for article links
            const links = document.querySelectorAll('a[href*="/"]');

            for (let link of links) {
                if (results.length >= 20) break;

                const headline = link.innerText?.trim();
                const url = link.href;

                // Filter for actual article headlines
                if (headline &&
                    headline.length > 20 &&
                    headline.length < 300 &&
                    !seen.has(headline) &&
                    !headline.includes('©') &&
                    !headline.includes('Subscribe') &&
                    !headline.includes('Menu') &&
                    url.includes('businessinsider.com/')) {

                    const timeEl = link.closest('article')?.querySelector('time') ||
                                 link.parentElement?.querySelector('time');
                    const time = timeEl?.getAttribute('datetime') || timeEl?.innerText || 'Recent';

                    results.push({ headline, url, time });
                    seen.add(headline);
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
            path: '/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/news_user/screenshots/forbes_homepage.png',
            fullPage: true
        });

        const headlines = await page.evaluate(() => {
            const results = [];
            const seen = new Set();

            // Try multiple strategies
            const articles = document.querySelectorAll('article, [class*="stream-item"], [class*="article"]');

            for (let article of articles) {
                if (results.length >= 20) break;

                const headlineEl = article.querySelector('h2, h3, a[href*="/sites/"]');
                const linkEl = article.querySelector('a') || headlineEl;

                if (headlineEl && linkEl) {
                    const headline = headlineEl.innerText?.trim();
                    const url = linkEl.href;

                    if (headline &&
                        headline.length > 20 &&
                        headline.length < 300 &&
                        !seen.has(headline) &&
                        url.includes('forbes.com/')) {

                        const timeEl = article.querySelector('time, [class*="date"]');
                        const time = timeEl?.getAttribute('datetime') || timeEl?.innerText || 'Recent';

                        results.push({ headline, url, time });
                        seen.add(headline);
                    }
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
            markdown += `${idx + 1}. **${item.time || 'Recent'}** - ${item.headline}\n`;
            markdown += `   - URL: ${item.url}\n\n`;
        });
    } else {
        markdown += '*No headlines could be extracted (verification required)*\n\n';
    }

    markdown += '### Business Insider\n';
    if (biHeadlines.length > 0) {
        biHeadlines.forEach((item, idx) => {
            markdown += `${idx + 1}. **${item.time || 'Recent'}** - ${item.headline}\n`;
            markdown += `   - URL: ${item.url}\n\n`;
        });
    } else {
        markdown += '*No headlines could be extracted*\n\n';
    }

    markdown += '### Forbes\n';
    if (forbesHeadlines.length > 0) {
        forbesHeadlines.forEach((item, idx) => {
            markdown += `${idx + 1}. **${item.time || 'Recent'}** - ${item.headline}\n`;
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
        viewport: { width: 1920, height: 1080 }
    });

    const page = await context.newPage();

    try {
        const wsjHeadlines = await scrapeWSJ(page);
        const biHeadlines = await scrapeBusinessInsider(page);
        const forbesHeadlines = await scrapeForbes(page);

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
