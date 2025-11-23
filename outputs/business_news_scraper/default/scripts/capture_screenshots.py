import asyncio
import base64
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

async def get_screenshot(url, output_path):
    """
    Capture a full-page screenshot of a given URL using Playwright.

    Args:
        url (str): The URL to capture
        output_path (str): Path to save the screenshot

    Returns:
        str: Base64-encoded screenshot data
    """
    print(f'Capturing screenshot for {url}')

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1920, "height": 1080, "device_scale_factor": 0.5})

        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=120000)
        except PlaywrightTimeoutError:
            print(f"TimeoutError: Failed to load {url} within the specified timeout.")
            await asyncio.sleep(2)
        except Exception as e:
            print(f"Error loading {url}: {e}")
            await asyncio.sleep(2)

        # Reload page for stability
        try:
            await page.reload(wait_until='domcontentloaded')
        except Exception as e:
            print(f"Error reloading page: {e}")

        # Capture full-page screenshot
        await page.screenshot(path=output_path, full_page=True)
        await browser.close()

        # Read and encode screenshot
        data = open(output_path, "rb").read()
        print(f'Screenshot done, {len(data)} bytes')
        encoded_data = base64.b64encode(data).decode('utf-8')
        print(f"Screenshot of size {len(data)} bytes saved to {output_path}")

        return encoded_data

async def main():
    urls = {
        "wsj": "https://www.wsj.com",
        "business_insider": "https://www.businessinsider.com",
        "forbes": "https://www.forbes.com"
    }

    for name, url in urls.items():
        output_path = f"/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/default/screenshots/{name}_homepage.png"
        try:
            await get_screenshot(url, output_path)
            print(f"Successfully captured {name}")
        except Exception as e:
            print(f"Error capturing {name}: {e}")

if __name__ == "__main__":
    asyncio.run(main())
