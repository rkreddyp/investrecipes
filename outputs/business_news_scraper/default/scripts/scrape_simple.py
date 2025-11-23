import asyncio
import json
from playwright.async_api import async_playwright
import re

async def scrape_site(url, site_name):
    """Generic scraper for news sites"""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        )
        page = await context.new_page()

        try:
            print(f"Loading {site_name}...")
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(3)

            # Get page content
            content = await page.content()

            # Try to extract using JavaScript
            headlines = await page.evaluate("""
                () => {
                    const results = [];
                    const seen = new Set();

                    // Common headline selectors
                    const selectors = [
                        'h1 a', 'h2 a', 'h3 a',
                        'article a[href*="article"]',
                        'article a[href*="story"]',
                        'a[class*="headline"]',
                        'a[class*="title"]',
                        '[data-testid*="headline"] a',
                        '.headline a',
                        '.title a'
                    ];

                    selectors.forEach(selector => {
                        try {
                            document.querySelectorAll(selector).forEach(el => {
                                const text = el.textContent?.trim();
                                const href = el.href;

                                // Filter criteria
                                if (text &&
                                    text.length > 20 &&
                                    text.length < 200 &&
                                    href &&
                                    !seen.has(text)) {

                                    seen.add(text);
                                    results.push({
                                        headline: text,
                                        url: href,
                                        date: ''
                                    });
                                }
                            });
                        } catch (e) {}
                    });

                    return results;
                }
            """)

            # Deduplicate and limit
            unique_headlines = []
            seen_text = set()
            for h in headlines:
                if h['headline'] not in seen_text:
                    seen_text.add(h['headline'])
                    unique_headlines.append(h)
                    if len(unique_headlines) >= 20:
                        break

            print(f"Found {len(unique_headlines)} headlines from {site_name}")
            await browser.close()
            return unique_headlines

        except Exception as e:
            print(f"Error scraping {site_name}: {e}")
            await browser.close()
            return []

async def main():
    sites = {
        'wsj': 'https://www.wsj.com',
        'business_insider': 'https://www.businessinsider.com',
        'forbes': 'https://www.forbes.com'
    }

    results = {}

    for name, url in sites.items():
        results[name] = await scrape_site(url, name)

    # Save results
    output_file = "/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/default/raw/headlines.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n=== Summary ===")
    for name, headlines in results.items():
        print(f"{name}: {len(headlines)} headlines")

if __name__ == "__main__":
    asyncio.run(main())
