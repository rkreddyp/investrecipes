import asyncio
import json
from playwright.async_api import async_playwright

async def scrape_wsj_rss():
    """Try to get WSJ headlines from their RSS feed or alternate URLs"""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        )
        page = await context.new_page()

        headlines = []

        try:
            # Try the main business section
            print("Trying WSJ business section...")
            await page.goto("https://www.wsj.com/news/business", wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(3)

            headlines = await page.evaluate("""
                () => {
                    const results = [];
                    const seen = new Set();

                    const selectors = [
                        'h3 a', 'h2 a',
                        'article a',
                        '[class*="headline"] a',
                    ];

                    selectors.forEach(selector => {
                        try {
                            document.querySelectorAll(selector).forEach(el => {
                                const text = el.textContent?.trim();
                                const href = el.href;

                                if (text &&
                                    text.length > 20 &&
                                    text.length < 200 &&
                                    href &&
                                    href.includes('wsj.com') &&
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

                    return results.slice(0, 20);
                }
            """)

            print(f"Found {len(headlines)} WSJ headlines")

        except Exception as e:
            print(f"Error scraping WSJ: {e}")

        await browser.close()
        return headlines

async def main():
    headlines = await scrape_wsj_rss()

    # Save results
    output_file = "/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/default/raw/wsj_headlines.json"
    with open(output_file, "w") as f:
        json.dump(headlines, f, indent=2)

    print(f"\nSaved {len(headlines)} WSJ headlines")

if __name__ == "__main__":
    asyncio.run(main())
