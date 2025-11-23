import asyncio
import base64
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

async def login_and_screenshot_finviz():
    """
    Log into Finviz.com and capture screenshot of the news section.
    """
    print('Starting Finviz scraper...')

    output_path = "/Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/default/screenshots/finviz_news.png"

    async with async_playwright() as p:
        # Launch browser with high-resolution viewport
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page(
            viewport={"width": 1920, "height": 1080, "device_scale_factor": 0.5}
        )

        try:
            # Step 1: Navigate to Finviz.com
            print('Navigating to Finviz.com...')
            await page.goto("https://www.finviz.com", wait_until="domcontentloaded", timeout=120000)
            await asyncio.sleep(2)

            # Step 2: Take initial screenshot to see the page
            await page.screenshot(path="/Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/default/screenshots/finviz_initial.png", full_page=False)
            print('Initial screenshot saved')

            # Step 3: Look for login button/link
            print('Looking for login button...')

            # Try common selectors for login
            login_selectors = [
                'a[href*="login"]',
                'a:has-text("Login")',
                'a:has-text("Sign In")',
                '.login',
                '#login'
            ]

            login_clicked = False
            for selector in login_selectors:
                try:
                    login_element = await page.wait_for_selector(selector, timeout=5000)
                    if login_element:
                        print(f'Found login element with selector: {selector}')
                        await login_element.click()
                        login_clicked = True
                        break
                except Exception as e:
                    continue

            if not login_clicked:
                print('Could not find login button, checking if already logged in or need to navigate to login page directly')
                await page.goto("https://finviz.com/login", wait_until="domcontentloaded", timeout=120000)

            # Wait for login form to appear
            await asyncio.sleep(2)

            # Step 4: Fill in credentials
            print('Filling in login credentials...')

            # Try to find email/username field
            email_selectors = [
                'input[name="email"]',
                'input[type="email"]',
                'input[name="username"]',
                'input[id="email"]'
            ]

            for selector in email_selectors:
                try:
                    email_field = await page.wait_for_selector(selector, timeout=5000)
                    if email_field:
                        print(f'Found email field: {selector}')
                        await email_field.fill("rkreddy@gmail.com")
                        break
                except Exception as e:
                    continue

            # Try to find password field
            password_selectors = [
                'input[name="password"]',
                'input[type="password"]',
                'input[id="password"]'
            ]

            for selector in password_selectors:
                try:
                    password_field = await page.wait_for_selector(selector, timeout=5000)
                    if password_field:
                        print(f'Found password field: {selector}')
                        await password_field.fill("FP33talak00ra**")
                        break
                except Exception as e:
                    continue

            # Take screenshot before submitting
            await page.screenshot(path="/Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/default/screenshots/finviz_login_form.png", full_page=False)
            print('Login form screenshot saved')

            # Step 5: Submit login form
            print('Submitting login form...')
            submit_selectors = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button:has-text("Login")',
                'button:has-text("Sign In")'
            ]

            for selector in submit_selectors:
                try:
                    submit_button = await page.wait_for_selector(selector, timeout=5000)
                    if submit_button:
                        print(f'Found submit button: {selector}')
                        await submit_button.click()
                        break
                except Exception as e:
                    continue

            # Step 6: Wait for login to complete
            print('Waiting for login to complete...')
            await asyncio.sleep(5)

            # Take screenshot after login
            await page.screenshot(path="/Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/default/screenshots/finviz_after_login.png", full_page=False)
            print('Post-login screenshot saved')

            # Step 7: Navigate to news section
            print('Looking for news section...')

            # Try to find and click news tab/link
            news_selectors = [
                'a[href*="news"]',
                'a:has-text("News")',
                '.news',
                '#news'
            ]

            news_found = False
            for selector in news_selectors:
                try:
                    news_element = await page.wait_for_selector(selector, timeout=5000)
                    if news_element:
                        print(f'Found news element: {selector}')
                        await news_element.click()
                        news_found = True
                        break
                except Exception as e:
                    continue

            if not news_found:
                print('News link not found, trying direct navigation...')
                await page.goto("https://finviz.com/news.ashx", wait_until="networkidle", timeout=120000)

            # Step 8: Wait for news section to fully load
            print('Waiting for news section to load...')
            await asyncio.sleep(3)

            # Step 9: Capture final screenshot of news section
            print('Capturing news section screenshot...')
            await page.screenshot(path=output_path, full_page=True)

            # Read screenshot data
            data = open(output_path, "rb").read()
            print(f'Screenshot saved: {len(data)} bytes')

            await browser.close()

            return {
                "success": True,
                "screenshot_path": output_path,
                "screenshot_size": len(data)
            }

        except PlaywrightTimeoutError as e:
            print(f"TimeoutError: {e}")
            await page.screenshot(path="/Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/default/screenshots/finviz_error.png", full_page=True)
            await browser.close()
            return {
                "success": False,
                "error": str(e)
            }
        except Exception as e:
            print(f"Error: {e}")
            await page.screenshot(path="/Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/default/screenshots/finviz_error.png", full_page=True)
            await browser.close()
            return {
                "success": False,
                "error": str(e)
            }

async def main():
    result = await login_and_screenshot_finviz()
    print("\nScraping Result:")
    print(f"Success: {result.get('success')}")
    if result.get('success'):
        print(f"Screenshot Path: {result.get('screenshot_path')}")
        print(f"Screenshot Size: {result.get('screenshot_size')} bytes")
    else:
        print(f"Error: {result.get('error')}")

if __name__ == "__main__":
    asyncio.run(main())
