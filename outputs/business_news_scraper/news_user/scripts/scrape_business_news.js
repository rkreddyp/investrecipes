const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function scrapeWSJ(page) {
    console.log('Navigating to WSJ...');
    await page.goto('https://www.wsj.com/', { waitUntil: 'networkidle', timeout: 60000 });

    // Take screenshot
    await page.screenshot({
        path: '/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/news_user/screenshots/wsj_homepage.png',
        fullPage: true
    });

    // Wait for content to load
    await page.waitForTimeout(3000);

    // Extract headlines
    const headlines = await page.evaluate(() => {
        const results = [];
        const articles = document.querySelectorAll('article, [data-module-name*="lead"], .WSJTheme--headline');

        for (let article of articles) {
            if (results.length >= 20) break;

            const headlineEl = article.querySelector('h2, h3, .WSJTheme--headline, [data-module-name*="headline"]');
            const linkEl = article.querySelector('a');
            const timeEl = article.querySelector('time, [data-timestamp], .timestamp');

            if (headlineEl && linkEl) {
                const headline = headlineEl.innerText.trim();
                const url = linkEl.href;
                const time = timeEl ? timeEl.getAttribute('datetime') || timeEl.innerText : '';

                if (headline && headline.length > 10) {
                    results.push({ headline, url, time });
                }
            }
        }

        return results;
    });

    console.log(`Found ${headlines.length} WSJ headlines`);
    return headlines.slice(0, 10);
}

async function scrapeBusinessInsider(page) {
    console.log('Navigating to Business Insider...');
    await page.goto('https://www.businessinsider.com/', { waitUntil: 'networkidle', timeout: 60000 });

    // Take screenshot
    await page.screenshot({
        path: '/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/news_user/screenshots/businessinsider_homepage.png',
        fullPage: true
    });

    await page.waitForTimeout(3000);

    const headlines = await page.evaluate(() => {
        const results = [];
        const articles = document.querySelectorAll('article, .tout-default, [data-e2e-name*="article"], .story-card');

        for (let article of articles) {
            if (results.length >= 20) break;

            const headlineEl = article.querySelector('h2, h3, .tout-title, [data-e2e-name*="headline"]');
            const linkEl = article.querySelector('a');
            const timeEl = article.querySelector('time, .byline-timestamp, [data-timestamp]');

            if (headlineEl && linkEl) {
                const headline = headlineEl.innerText.trim();
                const url = linkEl.href;
                const time = timeEl ? timeEl.getAttribute('datetime') || timeEl.innerText : '';

                if (headline && headline.length > 10) {
                    results.push({ headline, url, time });
                }
            }
        }

        return results;
    });

    console.log(`Found ${headlines.length} Business Insider headlines`);
    return headlines.slice(0, 10);
}

async function scrapeForbes(page) {
    console.log('Navigating to Forbes...');
    await page.goto('https://www.forbes.com/', { waitUntil: 'networkidle', timeout: 60000 });

    // Take screenshot
    await page.screenshot({
        path: '/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/news_user/screenshots/forbes_homepage.png',
        fullPage: true
    });

    await page.waitForTimeout(3000);

    const headlines = await page.evaluate(() => {
        const results = [];
        const articles = document.querySelectorAll('article, .stream-item, [data-module*="article"]');

        for (let article of articles) {
            if (results.length >= 20) break;

            const headlineEl = article.querySelector('h2, h3, .article-headline, .stream-item__title');
            const linkEl = article.querySelector('a');
            const timeEl = article.querySelector('time, .stream-item__date, [data-time]');

            if (headlineEl && linkEl) {
                const headline = headlineEl.innerText.trim();
                const url = linkEl.href;
                const time = timeEl ? timeEl.getAttribute('datetime') || timeEl.innerText : '';

                if (headline && headline.length > 10) {
                    results.push({ headline, url, time });
                }
            }
        }

        return results;
    });

    console.log(`Found ${headlines.length} Forbes headlines`);
    return headlines.slice(0, 10);
}

function formatMarkdown(wsjHeadlines, biHeadlines, forbesHeadlines) {
    let markdown = '## Business News Sources\n\n';

    markdown += '### Wall Street Journal\n';
    wsjHeadlines.forEach((item, idx) => {
        markdown += `${idx + 1}. **${item.time || 'Recent'}** - ${item.headline}\n`;
        markdown += `   - URL: ${item.url}\n\n`;
    });

    markdown += '### Business Insider\n';
    biHeadlines.forEach((item, idx) => {
        markdown += `${idx + 1}. **${item.time || 'Recent'}** - ${item.headline}\n`;
        markdown += `   - URL: ${item.url}\n\n`;
    });

    markdown += '### Forbes\n';
    forbesHeadlines.forEach((item, idx) => {
        markdown += `${idx + 1}. **${item.time || 'Recent'}** - ${item.headline}\n`;
        markdown += `   - URL: ${item.url}\n\n`;
    });

    return markdown;
}

async function main() {
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
        userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
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
