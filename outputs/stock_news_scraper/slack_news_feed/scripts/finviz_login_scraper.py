import asyncio
import base64
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

async def login_and_screenshot_finviz():
    """
    Log into Finviz.com and capture screenshot of news section.

    Returns:
        str: Path to saved screenshot
    """
    print('Starting Finviz login and screenshot capture...')

    screenshot_path = "/Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/slack_news_feed/screenshots/finviz_news.png"

    async with async_playwright() as p:
        # Launch browser in headed mode for better stability
        browser = await p.chromium.launch(headless=False)

        # Create context with high-resolution viewport
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=0.5,
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        )

        # Set default timeout
        context.set_default_timeout(120000)

        page = await context.new_page()

        try:
            # Step 1: Navigate to Finviz.com
            print('Step 1: Navigating to Finviz.com...')
            try:
                await page.goto("https://finviz.com/", wait_until="domcontentloaded", timeout=120000)
            except PlaywrightTimeoutError:
                print('Navigation timeout, but continuing...')
            await asyncio.sleep(3)

            # Step 2: Take initial screenshot to see page structure
            print('Step 2: Taking initial screenshot...')
            try:
                await page.screenshot(path="/Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/slack_news_feed/screenshots/finviz_initial.png", full_page=True, timeout=60000)
            except PlaywrightTimeoutError:
                print('Initial screenshot timeout, skipping...')

            # Step 3: Look for login link/button - try multiple selectors
            print('Step 3: Looking for login button...')

            # Common login selectors to try
            login_selectors = [
                'a[href*="login"]',
                'a:has-text("Login")',
                'a:has-text("Sign In")',
                'button:has-text("Login")',
                '#login',
                '.login'
            ]

            login_element = None
            for selector in login_selectors:
                try:
                    login_element = await page.wait_for_selector(selector, timeout=5000, state="visible")
                    if login_element:
                        print(f'Found login element with selector: {selector}')
                        break
                except:
                    continue

            if login_element:
                # Step 4: Click login button
                print('Step 4: Clicking login button...')
                await login_element.click()
                await asyncio.sleep(2)
            else:
                # Try navigating directly to login page
                print('Login button not found, trying direct navigation to login page...')
                try:
                    await page.goto("https://finviz.com/login.ashx", wait_until="domcontentloaded", timeout=120000)
                except PlaywrightTimeoutError:
                    print('Login page navigation timeout, but continuing...')
                await asyncio.sleep(2)

            # Step 5: Wait for login form and fill credentials
            print('Step 5: Filling in credentials...')

            # Try multiple email field selectors
            email_selectors = ['input[name="email"]', 'input[type="email"]', 'input#email']
            for selector in email_selectors:
                try:
                    email_field = await page.wait_for_selector(selector, timeout=5000, state="visible")
                    if email_field:
                        await email_field.fill("rkreddy@gmail.com")
                        print('Email filled successfully')
                        break
                except:
                    continue

            # Try multiple password field selectors
            password_selectors = ['input[name="password"]', 'input[type="password"]', 'input#password']
            for selector in password_selectors:
                try:
                    password_field = await page.wait_for_selector(selector, timeout=5000, state="visible")
                    if password_field:
                        await password_field.fill("FP33talak00ra*")
                        print('Password filled successfully')
                        break
                except:
                    continue

            # Step 6: Submit login form
            print('Step 6: Submitting login form...')

            # Try multiple submit button selectors
            submit_selectors = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button:has-text("Login")',
                'button:has-text("Sign In")',
                'input[value="Login"]'
            ]

            for selector in submit_selectors:
                try:
                    submit_button = await page.wait_for_selector(selector, timeout=5000, state="visible")
                    if submit_button:
                        await submit_button.click()
                        print('Login form submitted')
                        break
                except:
                    continue

            # Wait for login to complete
            await asyncio.sleep(5)

            # Step 7: Take screenshot after login
            print('Step 7: Taking post-login screenshot...')
            try:
                await page.screenshot(path="/Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/slack_news_feed/screenshots/finviz_post_login.png", full_page=True, timeout=60000)
            except PlaywrightTimeoutError:
                print('Post-login screenshot timeout, skipping...')

            # Step 8: Navigate to news section
            print('Step 8: Navigating to news section...')

            # Try to find and click News tab/link
            news_selectors = [
                'a[href*="news"]',
                'a:has-text("News")',
                'nav a:has-text("News")',
                '.tab:has-text("News")'
            ]

            news_found = False
            for selector in news_selectors:
                try:
                    news_link = await page.wait_for_selector(selector, timeout=5000, state="visible")
                    if news_link:
                        await news_link.click()
                        print(f'Clicked News link with selector: {selector}')
                        news_found = True
                        break
                except:
                    continue

            if not news_found:
                # Try direct navigation to news page
                print('News link not found, trying direct navigation...')
                try:
                    await page.goto("https://finviz.com/news.ashx", wait_until="networkidle", timeout=120000)
                except PlaywrightTimeoutError:
                    print('News page navigation timeout, but continuing...')

            # Wait for news section to load
            await asyncio.sleep(5)

            # Step 9: Wait for page to be fully loaded
            print('Step 9: Waiting for news section to load completely...')
            try:
                await page.wait_for_load_state("networkidle", timeout=60000)
            except PlaywrightTimeoutError:
                print("TimeoutError: Page still loading, continuing anyway...")

            # Step 10: Capture final screenshot of news section
            print('Step 10: Capturing final screenshot of news section...')
            await page.screenshot(path=screenshot_path, full_page=True, timeout=120000)

            # Read and encode screenshot
            data = open(screenshot_path, "rb").read()
            print(f'Screenshot saved successfully: {len(data)} bytes')

        except Exception as e:
            print(f"Error during login/screenshot process: {e}")
            # Take error screenshot for debugging
            try:
                await page.screenshot(path="/Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/slack_news_feed/screenshots/finviz_error.png", full_page=False, timeout=30000)
            except:
                print('Could not capture error screenshot')
            raise

        finally:
            await browser.close()

    return screenshot_path

# Run the async function
async def main():
    screenshot_path = await login_and_screenshot_finviz()
    print(f"\n=== COMPLETED ===")
    print(f"Screenshot saved to: {screenshot_path}")
    return screenshot_path

if __name__ == "__main__":
    asyncio.run(main())
