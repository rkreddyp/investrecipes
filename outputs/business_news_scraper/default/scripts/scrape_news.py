import asyncio
import json
from playwright.async_api import async_playwright

async def scrape_wsj():
    """Scrape Wall Street Journal headlines"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})

        try:
            # Try to access WSJ
            await page.goto("https://www.wsj.com", wait_until="networkidle", timeout=60000)
            await asyncio.sleep(5)

            # Take a high-res screenshot
            await page.screenshot(path="/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/default/screenshots/wsj_final.png", full_page=True)

            # Extract headlines
            headlines = await page.evaluate("""
                () => {
                    const articles = [];
                    const headlineSelectors = [
                        'article h2', 'article h3',
                        '.WSJTheme--headline--unZqjb45',
                        '[class*="headline"]',
                        'a[class*="Headline"]'
                    ];

                    headlineSelectors.forEach(selector => {
                        document.querySelectorAll(selector).forEach(el => {
                            const text = el.innerText?.trim();
                            const link = el.closest('a')?.href;
                            if (text && text.length > 10) {
                                articles.push({
                                    headline: text,
                                    url: link || '',
                                    date: ''
                                });
                            }
                        });
                    });

                    return articles.slice(0, 20);
                }
            """)

            await browser.close()
            return headlines

        except Exception as e:
            print(f"Error scraping WSJ: {e}")
            await browser.close()
            return []

async def scrape_business_insider():
    """Scrape Business Insider headlines"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})

        try:
            await page.goto("https://www.businessinsider.com", wait_until="networkidle", timeout=60000)
            await asyncio.sleep(5)

            # Take screenshot
            await page.screenshot(path="/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/default/screenshots/business_insider_final.png", full_page=True)

            # Extract headlines
            headlines = await page.evaluate("""
                () => {
                    const articles = [];
                    const headlineSelectors = [
                        'article h2', 'article h3',
                        '.tout-title-link',
                        '[data-e2e-name="tout-title-link"]',
                        'a[class*="headline"]',
                        '.story-link'
                    ];

                    headlineSelectors.forEach(selector => {
                        document.querySelectorAll(selector).forEach(el => {
                            const text = el.innerText?.trim();
                            const link = el.href || el.closest('a')?.href;
                            if (text && text.length > 10) {
                                articles.push({
                                    headline: text,
                                    url: link || '',
                                    date: ''
                                });
                            }
                        });
                    });

                    return articles.slice(0, 20);
                }
            """)

            await browser.close()
            return headlines

        except Exception as e:
            print(f"Error scraping Business Insider: {e}")
            await browser.close()
            return []

async def scrape_forbes():
    """Scrape Forbes headlines"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})

        try:
            await page.goto("https://www.forbes.com", wait_until="networkidle", timeout=60000)
            await asyncio.sleep(5)

            # Take screenshot
            await page.screenshot(path="/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/default/screenshots/forbes_final.png", full_page=True)

            # Extract headlines
            headlines = await page.evaluate("""
                () => {
                    const articles = [];
                    const headlineSelectors = [
                        'article h2', 'article h3',
                        '.stream-item__title',
                        '[class*="headline"]',
                        'a[class*="HeadlineLink"]'
                    ];

                    headlineSelectors.forEach(selector => {
                        document.querySelectorAll(selector).forEach(el => {
                            const text = el.innerText?.trim();
                            const link = el.href || el.closest('a')?.href;
                            if (text && text.length > 10) {
                                articles.push({
                                    headline: text,
                                    url: link || '',
                                    date: ''
                                });
                            }
                        });
                    });

                    return articles.slice(0, 20);
                }
            """)

            await browser.close()
            return headlines

        except Exception as e:
            print(f"Error scraping Forbes: {e}")
            await browser.close()
            return []

async def main():
    results = {}

    print("Scraping Wall Street Journal...")
    results['wsj'] = await scrape_wsj()

    print("Scraping Business Insider...")
    results['business_insider'] = await scrape_business_insider()

    print("Scraping Forbes...")
    results['forbes'] = await scrape_forbes()

    # Save results
    with open("/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/default/raw/headlines.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults:")
    print(f"WSJ: {len(results['wsj'])} headlines")
    print(f"Business Insider: {len(results['business_insider'])} headlines")
    print(f"Forbes: {len(results['forbes'])} headlines")

if __name__ == "__main__":
    asyncio.run(main())
