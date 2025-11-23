const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function scrapeWebsite(url, name, outputDir) {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();

    try {
        console.log(`Navigating to ${name}...`);
        await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });

        // Wait for content to load
        await page.waitForTimeout(3000);

        // Take screenshot
        const screenshotPath = path.join(outputDir, 'screenshots', `${name.toLowerCase().replace(/\s/g, '_')}.png`);
        await page.screenshot({ path: screenshotPath, fullPage: true });
        console.log(`Screenshot saved: ${screenshotPath}`);

        // Extract headlines based on site
        let headlines = [];

        if (name === 'TechCrunch') {
            headlines = await page.evaluate(() => {
                const items = [];
                // Look for article links
                const articles = document.querySelectorAll('article, .post-block, a[href*="/2025/"], a[href*="/2024/"]');

                articles.forEach((article, idx) => {
                    if (items.length >= 10) return;

                    let title = '';
                    let url = '';
                    let date = '';

                    // Try to find title
                    const titleEl = article.querySelector('h2, h3, .post-block__title, [class*="title"]');
                    if (titleEl) {
                        title = titleEl.textContent.trim();
                    } else if (article.tagName === 'A') {
                        title = article.textContent.trim();
                    }

                    // Try to find URL
                    const linkEl = article.querySelector('a') || (article.tagName === 'A' ? article : null);
                    if (linkEl) {
                        url = linkEl.href;
                    }

                    // Try to find date
                    const dateEl = article.querySelector('time, .post-block__time, [class*="date"]');
                    if (dateEl) {
                        date = dateEl.textContent.trim();
                    }

                    if (title && title.length > 10 && url && url.includes('techcrunch.com')) {
                        items.push({ title, url, date });
                    }
                });

                return items;
            });
        } else if (name === 'The Verge') {
            headlines = await page.evaluate(() => {
                const items = [];
                const articles = document.querySelectorAll('article, .duet--article, a[href*="/2025/"], a[href*="/2024/"]');

                articles.forEach((article, idx) => {
                    if (items.length >= 10) return;

                    let title = '';
                    let url = '';
                    let date = '';

                    const titleEl = article.querySelector('h2, h3, .duet--article--title, [class*="title"]');
                    if (titleEl) {
                        title = titleEl.textContent.trim();
                    } else if (article.tagName === 'A') {
                        title = article.textContent.trim();
                    }

                    const linkEl = article.querySelector('a') || (article.tagName === 'A' ? article : null);
                    if (linkEl) {
                        url = linkEl.href;
                    }

                    const dateEl = article.querySelector('time, [class*="date"]');
                    if (dateEl) {
                        date = dateEl.textContent.trim();
                    }

                    if (title && title.length > 10 && url && url.includes('theverge.com')) {
                        items.push({ title, url, date });
                    }
                });

                return items;
            });
        } else if (name === 'Ars Technica') {
            headlines = await page.evaluate(() => {
                const items = [];
                const articles = document.querySelectorAll('article, header, a[href*="/2025/"], a[href*="/2024/"]');

                articles.forEach((article, idx) => {
                    if (items.length >= 10) return;

                    let title = '';
                    let url = '';
                    let date = '';

                    const titleEl = article.querySelector('h2, h3, h4, [class*="title"]');
                    if (titleEl) {
                        title = titleEl.textContent.trim();
                    } else if (article.tagName === 'A') {
                        title = article.textContent.trim();
                    }

                    const linkEl = article.querySelector('a') || (article.tagName === 'A' ? article : null);
                    if (linkEl) {
                        url = linkEl.href;
                    }

                    const dateEl = article.querySelector('time, [class*="date"]');
                    if (dateEl) {
                        date = dateEl.textContent.trim();
                    }

                    if (title && title.length > 10 && url && url.includes('arstechnica.com')) {
                        items.push({ title, url, date });
                    }
                });

                return items;
            });
        }

        // Limit to 10 headlines
        headlines = headlines.slice(0, 10);

        console.log(`Extracted ${headlines.length} headlines from ${name}`);

        await browser.close();
        return headlines;

    } catch (error) {
        console.error(`Error scraping ${name}:`, error.message);
        await browser.close();
        return [];
    }
}

async function main() {
    const baseDir = '/Users/venkat/workfolder/playwright-min/outputs/tech_news_scraper/customer';

    const websites = [
        { url: 'https://techcrunch.com', name: 'TechCrunch' },
        { url: 'https://www.theverge.com', name: 'The Verge' },
        { url: 'https://arstechnica.com', name: 'Ars Technica' }
    ];

    const allHeadlines = {};

    for (const site of websites) {
        const headlines = await scrapeWebsite(site.url, site.name, baseDir);
        allHeadlines[site.name] = headlines;
    }

    // Save raw data as JSON
    const jsonPath = path.join(baseDir, 'raw', 'tech_headlines.json');
    fs.writeFileSync(jsonPath, JSON.stringify(allHeadlines, null, 2));
    console.log(`\nRaw data saved to: ${jsonPath}`);

    // Generate markdown report
    let report = '# Tech News Headlines\n\n';
    report += `Generated: ${new Date().toISOString()}\n\n`;

    for (const [source, headlines] of Object.entries(allHeadlines)) {
        report += `## ${source}\n\n`;
        headlines.forEach((item, idx) => {
            report += `${idx + 1}. `;
            if (item.date) report += `**[${item.date}]** - `;
            report += `${item.title}\n`;
            if (item.url) report += `   - URL: ${item.url}\n`;
            report += '\n';
        });
        report += '\n';
    }

    const reportPath = path.join(baseDir, 'reports', 'tech_news_report.md');
    fs.writeFileSync(reportPath, report);
    console.log(`Report saved to: ${reportPath}`);
}

main().catch(console.error);
