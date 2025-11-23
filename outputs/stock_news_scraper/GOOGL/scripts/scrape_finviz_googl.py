import asyncio
import base64
import json
from playwright.async_api import async_playwright
import playwright._impl._api_types
from datetime import datetime

async def get_screenshot_finviz(ticker, output_path):
    """
    Capture screenshot of Finviz news page for a specific ticker.
    Uses webpage-screenshotter skill implementation with networkidle wait.

    Args:
        ticker (str): Stock ticker symbol
        output_path (str): Path to save screenshot

    Returns:
        str: Base64-encoded screenshot data
    """
    url = f"https://finviz.com/quote.ashx?t={ticker}"
    print(f'Capturing Finviz news for {ticker} from {url}')

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080, "device_scale_factor": 0.5})

        try:
            # Navigate to Finviz quote page (contains news section)
            await page.goto(url, wait_until="networkidle", timeout=120000)
            print(f"Page loaded successfully for {ticker}")
        except playwright._impl._api_types.TimeoutError:
            print(f"TimeoutError: Failed to load {url} within the specified timeout.")
            await asyncio.sleep(2)

        # Wait for news table to be visible
        try:
            await page.wait_for_selector("table.fullview-news-outer", timeout=10000)
            print("News section found and loaded")
        except:
            print("Warning: News section selector not found, proceeding anyway")

        # Capture full-page screenshot
        await page.screenshot(path=output_path, full_page=True)
        await browser.close()

        # Read and encode screenshot
        data = open(output_path, "rb").read()
        print(f'Screenshot saved to {output_path}, size: {len(data)} bytes')
        encoded_data = base64.b64encode(data).decode('utf-8')

        return encoded_data

async def extract_news_data(ticker):
    """
    Extract news headlines from Finviz using Playwright.

    Args:
        ticker (str): Stock ticker symbol

    Returns:
        list: List of news items with headline, date, and source
    """
    url = f"https://finviz.com/quote.ashx?t={ticker}"
    print(f'Extracting news data for {ticker}')

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080, "device_scale_factor": 0.5})

        try:
            await page.goto(url, wait_until="networkidle", timeout=120000)

            # Wait for news table
            await page.wait_for_selector("table.fullview-news-outer", timeout=10000)

            # Extract news items using JavaScript
            news_items = await page.evaluate("""
                () => {
                    const newsTable = document.querySelector('table.fullview-news-outer');
                    if (!newsTable) return [];

                    const rows = newsTable.querySelectorAll('tr');
                    const news = [];

                    rows.forEach(row => {
                        const dateCell = row.querySelector('td:first-child');
                        const linkCell = row.querySelector('td:last-child a');

                        if (dateCell && linkCell) {
                            news.push({
                                date: dateCell.textContent.trim(),
                                headline: linkCell.textContent.trim(),
                                url: linkCell.href,
                                source: linkCell.hostname || 'Unknown'
                            });
                        }
                    });

                    return news;
                }
            """)

            await browser.close()
            print(f"Extracted {len(news_items)} news items")
            return news_items

        except Exception as e:
            print(f"Error extracting news data: {e}")
            await browser.close()
            return []

async def main():
    ticker = "GOOGL"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Define output paths
    screenshot_path = f"/Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/{ticker}/screenshots/finviz_news_{timestamp}.png"
    raw_data_path = f"/Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/{ticker}/raw/news_data_{timestamp}.json"

    # Capture screenshot
    print("Step 1: Capturing screenshot...")
    await get_screenshot_finviz(ticker, screenshot_path)

    # Extract news data
    print("\nStep 2: Extracting news data...")
    news_items = await extract_news_data(ticker)

    # Save raw data
    if news_items:
        with open(raw_data_path, 'w') as f:
            json.dump({
                'ticker': ticker,
                'company': 'Alphabet Inc. (Google)',
                'timestamp': timestamp,
                'news_count': len(news_items),
                'news_items': news_items
            }, f, indent=2)
        print(f"\nNews data saved to {raw_data_path}")

        # Print summary
        print(f"\n=== GOOGL News Summary ===")
        print(f"Total news items: {len(news_items)}")
        print(f"\nLatest headlines:")
        for i, item in enumerate(news_items[:10], 1):
            print(f"{i}. [{item['date']}] {item['headline']}")
    else:
        print("No news items extracted")

    print(f"\nScreenshot saved: {screenshot_path}")
    print(f"Raw data saved: {raw_data_path}")

if __name__ == "__main__":
    asyncio.run(main())
