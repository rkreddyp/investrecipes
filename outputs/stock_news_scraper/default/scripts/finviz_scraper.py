import asyncio
import base64
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

async def login_and_capture_finviz():
    """
    Log into Finviz.com and capture screenshots of the stock news section.

    Uses credentials:
    - Email: rkreddy@gmail.com
    - Password: FP33talak00ra*
    """
    print('Starting Finviz login and screenshot capture...')

    async with async_playwright() as p:
        # Launch browser in headed mode for better compatibility
        browser = await p.chromium.launch(headless=False)

        # Create page with high-resolution viewport
        page = await browser.new_page(
            viewport={"width": 1920, "height": 1080, "device_scale_factor": 0.5}
        )

        try:
            # Step 1: Navigate to Finviz homepage
            print('Navigating to Finviz.com...')
            await page.goto("https://www.finviz.com", wait_until="domcontentloaded", timeout=120000)

            # Wait a bit for page to settle
            await asyncio.sleep(5)

            # Step 2: Take initial screenshot
            print('Taking initial screenshot...')
            await page.screenshot(
                path="/Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/default/screenshots/01_homepage.png",
                full_page=True
            )

            # Step 3: Look for login link/button and click it
            print('Looking for login button...')

            # Try multiple possible selectors for login button
            login_selectors = [
                'a[href*="login"]',
                'a:has-text("Login")',
                'a:has-text("Sign In")',
                'text=Login',
                'text=Sign In',
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
                        await asyncio.sleep(2)
                        break
                except Exception as e:
                    print(f'Selector {selector} failed: {e}')
                    continue

            if not login_clicked:
                print('Could not find login button with standard selectors. Checking page content...')
                # Take screenshot to see current state
                await page.screenshot(
                    path="/Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/default/screenshots/02_login_search.png",
                    full_page=True
                )

            # Step 4: Wait for login form to appear
            print('Waiting for login form...')
            await asyncio.sleep(3)

            # Step 5: Fill in credentials
            print('Filling in credentials...')

            # Try to find email/username field
            email_selectors = [
                'input[type="email"]',
                'input[name="email"]',
                'input[name="username"]',
                'input[id*="email"]',
                'input[id*="username"]',
                'input[placeholder*="email" i]',
                'input[placeholder*="username" i]'
            ]

            email_filled = False
            for selector in email_selectors:
                try:
                    email_field = await page.wait_for_selector(selector, timeout=5000)
                    if email_field:
                        print(f'Found email field with selector: {selector}')
                        await email_field.fill('rkreddy@gmail.com')
                        email_filled = True
                        break
                except Exception as e:
                    print(f'Email selector {selector} failed: {e}')
                    continue

            # Try to find password field
            password_selectors = [
                'input[type="password"]',
                'input[name="password"]',
                'input[id*="password"]',
                'input[placeholder*="password" i]'
            ]

            password_filled = False
            for selector in password_selectors:
                try:
                    password_field = await page.wait_for_selector(selector, timeout=5000)
                    if password_field:
                        print(f'Found password field with selector: {selector}')
                        await password_field.fill('FP33talak00ra*')
                        password_filled = True
                        break
                except Exception as e:
                    print(f'Password selector {selector} failed: {e}')
                    continue

            # Take screenshot of filled form
            await page.screenshot(
                path="/Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/default/screenshots/03_login_form_filled.png",
                full_page=True
            )

            # Step 6: Submit login form
            print('Submitting login form...')

            # Try to find and click submit button
            submit_selectors = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button:has-text("Login")',
                'button:has-text("Sign In")',
                'button:has-text("Log In")',
                'text=Login',
                'text=Sign In'
            ]

            submit_clicked = False
            for selector in submit_selectors:
                try:
                    submit_button = await page.wait_for_selector(selector, timeout=5000)
                    if submit_button:
                        print(f'Found submit button with selector: {selector}')
                        await submit_button.click()
                        submit_clicked = True
                        break
                except Exception as e:
                    print(f'Submit selector {selector} failed: {e}')
                    continue

            # Step 7: Wait for login to complete
            print('Waiting for login to complete...')
            await asyncio.sleep(5)

            # Take screenshot after login
            await page.screenshot(
                path="/Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/default/screenshots/04_after_login.png",
                full_page=True
            )

            # Step 8: Navigate to news section
            print('Looking for news section...')

            # Try to find and click news tab/link
            news_selectors = [
                'a[href*="news"]',
                'a:has-text("News")',
                'text=News',
                '.tab-link:has-text("News")'
            ]

            news_found = False
            for selector in news_selectors:
                try:
                    news_link = await page.wait_for_selector(selector, timeout=5000)
                    if news_link:
                        print(f'Found news link with selector: {selector}')
                        await news_link.click()
                        news_found = True
                        await asyncio.sleep(3)
                        break
                except Exception as e:
                    print(f'News selector {selector} failed: {e}')
                    continue

            if not news_found:
                print('News section might already be visible or at different location')

            # Step 9: Wait for news section to fully load
            print('Waiting for news section to load...')
            await asyncio.sleep(5)

            # Step 10: Capture final screenshot of news section
            print('Capturing final screenshot of news section...')
            await page.screenshot(
                path="/Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/default/screenshots/05_finviz_news.png",
                full_page=True
            )

            print('Screenshot capture complete!')

        except PlaywrightTimeoutError as e:
            print(f"TimeoutError: {e}")
            # Take error screenshot
            try:
                await page.screenshot(
                    path="/Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/default/screenshots/error_timeout.png",
                    full_page=True
                )
            except:
                pass

        except Exception as e:
            print(f"Error occurred: {e}")
            # Take error screenshot
            try:
                await page.screenshot(
                    path="/Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/default/screenshots/error_general.png",
                    full_page=True
                )
            except:
                pass

        finally:
            # Close browser
            print('Closing browser...')
            await browser.close()

# Run the async function
if __name__ == "__main__":
    asyncio.run(login_and_capture_finviz())
