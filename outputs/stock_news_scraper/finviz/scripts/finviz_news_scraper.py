import asyncio
import json
from playwright.async_api import async_playwright, TimeoutError
from datetime import datetime

# Finviz credentials
EMAIL = "rkreddy@gmail.com"
PASSWORD = "FP33talak00ra*"

async def take_screenshot_safe(page, path, description):
    """Helper function to take screenshots with error handling"""
    try:
        await page.screenshot(path=path, full_page=True, timeout=60000)
        print(f'{description} screenshot saved: {path}')
        return True
    except Exception as e:
        print(f'Warning: Failed to capture {description} screenshot: {e}')
        return False

async def login_and_screenshot_finviz():
    """
    Login to Finviz.com and capture screenshots of the news section.
    Returns extracted news headlines and metadata.
    """
    print('Starting Finviz news scraper...')

    async with async_playwright() as p:
        # Launch browser in headed mode for better Cloudflare bypass
        browser = await p.chromium.launch(headless=False)

        # Create context with high-resolution viewport
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080, "device_scale_factor": 0.5},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        )

        page = await context.new_page()

        try:
            # Step 1: Navigate to Finviz homepage
            print('Step 1: Navigating to Finviz.com...')
            try:
                await page.goto("https://www.finviz.com", wait_until="load", timeout=120000)
            except TimeoutError:
                print("Timeout on initial load, continuing...")
            await asyncio.sleep(3)

            await take_screenshot_safe(page, "/Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/finviz/screenshots/01_homepage.png", "Homepage")

            # Step 2: Locate and click login link
            print('Step 2: Looking for login link...')

            # Try multiple selectors for login link
            login_selectors = [
                'a[href*="login"]',
                'a:has-text("Login")',
                'a:has-text("Sign In")',
                'a:has-text("login")',
                'a[class*="login"]',
                'a.login',
                '#login-link'
            ]

            login_clicked = False
            for selector in login_selectors:
                try:
                    login_link = await page.query_selector(selector)
                    if login_link and await login_link.is_visible():
                        print(f'Found login link with selector: {selector}')
                        await login_link.click()
                        login_clicked = True
                        await asyncio.sleep(2)
                        break
                except Exception as e:
                    continue

            if not login_clicked:
                print('Could not find login link, trying direct URL')
                try:
                    await page.goto("https://finviz.com/login.ashx", wait_until="load", timeout=120000)
                except TimeoutError:
                    print("Timeout on login page load, continuing...")
                await asyncio.sleep(2)

            await take_screenshot_safe(page, "/Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/finviz/screenshots/02_login_page.png", "Login page")

            # Step 3: Fill in login credentials
            print('Step 3: Filling login credentials...')

            # Try multiple selectors for email/username field
            email_selectors = [
                'input[name="email"]',
                'input[type="email"]',
                'input[name="username"]',
                'input[id="email"]',
                'input[placeholder*="email" i]',
                'input[placeholder*="Email"]'
            ]

            email_filled = False
            for selector in email_selectors:
                try:
                    email_field = await page.query_selector(selector)
                    if email_field and await email_field.is_visible():
                        print(f'Found email field with selector: {selector}')
                        await email_field.click()
                        await email_field.fill(EMAIL)
                        email_filled = True
                        break
                except Exception as e:
                    continue

            if not email_filled:
                print('WARNING: Could not find email field')

            # Try multiple selectors for password field
            password_selectors = [
                'input[name="password"]',
                'input[type="password"]',
                'input[id="password"]',
                'input[placeholder*="password" i]'
            ]

            password_filled = False
            for selector in password_selectors:
                try:
                    password_field = await page.query_selector(selector)
                    if password_field and await password_field.is_visible():
                        print(f'Found password field with selector: {selector}')
                        await password_field.click()
                        await password_field.fill(PASSWORD)
                        password_filled = True
                        break
                except Exception as e:
                    continue

            if not password_filled:
                print('WARNING: Could not find password field')

            await asyncio.sleep(1)

            await take_screenshot_safe(page, "/Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/finviz/screenshots/03_credentials_filled.png", "Credentials filled")

            # Step 4: Submit login form
            print('Step 4: Submitting login form...')

            # Try multiple selectors for submit button
            submit_selectors = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button:has-text("Login")',
                'button:has-text("Sign In")',
                'button:has-text("Log In")',
                'input[value*="Login" i]',
                'input[value*="Sign In" i]'
            ]

            submit_clicked = False
            for selector in submit_selectors:
                try:
                    submit_button = await page.query_selector(selector)
                    if submit_button and await submit_button.is_visible():
                        print(f'Found submit button with selector: {selector}')
                        await submit_button.click()
                        submit_clicked = True
                        break
                except Exception as e:
                    continue

            if not submit_clicked:
                print('Could not find submit button, trying to press Enter on password field')
                for selector in password_selectors:
                    try:
                        password_field = await page.query_selector(selector)
                        if password_field:
                            await password_field.press('Enter')
                            print('Pressed Enter on password field')
                            break
                    except Exception as e:
                        continue

            # Wait for navigation after login
            print('Waiting for login to complete...')
            await asyncio.sleep(5)

            await take_screenshot_safe(page, "/Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/finviz/screenshots/04_after_login.png", "After login")

            # Step 5: Navigate to news section
            print('Step 5: Navigating to news section...')

            current_url = page.url
            print(f'Current URL: {current_url}')

            # Try direct navigation to news page
            print('Navigating directly to news page...')
            try:
                await page.goto("https://finviz.com/news.ashx", wait_until="networkidle", timeout=120000)
            except TimeoutError:
                print("Timeout on news page load, continuing...")
            await asyncio.sleep(3)

            # Wait for news section to fully load
            try:
                await page.wait_for_load_state("networkidle", timeout=60000)
            except TimeoutError:
                print("Timeout waiting for network idle, continuing...")
            await asyncio.sleep(2)

            await take_screenshot_safe(page, "/Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/finviz/screenshots/05_news_section.png", "News section")

            # Step 6: Extract news headlines and data
            print('Step 6: Extracting news data...')

            # Extract page HTML for debugging
            html_content = await page.content()
            with open('/Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/finviz/raw/page_source.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
            print('Page source saved for debugging')

            # Extract news using JavaScript with multiple strategies
            news_items = await page.evaluate('''() => {
                const items = [];

                // Strategy 1: Look for news tables
                const newsTables = document.querySelectorAll('table.news-table, table.fullview-news-outer, table[id*="news"]');
                console.log('Found news tables:', newsTables.length);

                newsTables.forEach(table => {
                    const rows = table.querySelectorAll('tr');
                    rows.forEach(row => {
                        const link = row.querySelector('a');
                        const timeCell = row.querySelector('td:first-child');

                        if (link && link.href && !link.href.includes('javascript')) {
                            const headline = link.textContent.trim();
                            if (headline.length > 5) {
                                items.push({
                                    headline: headline,
                                    url: link.href,
                                    time: timeCell ? timeCell.textContent.trim() : '',
                                    source: link.hostname || ''
                                });
                            }
                        }
                    });
                });

                // Strategy 2: Look for news container divs
                if (items.length === 0) {
                    const newsContainers = document.querySelectorAll('.news-container, .news-item, [class*="news"]');
                    console.log('Found news containers:', newsContainers.length);

                    newsContainers.forEach(container => {
                        const links = container.querySelectorAll('a');
                        links.forEach(link => {
                            if (link.href && !link.href.includes('javascript')) {
                                const headline = link.textContent.trim();
                                if (headline.length > 10) {
                                    items.push({
                                        headline: headline,
                                        url: link.href,
                                        time: '',
                                        source: link.hostname || ''
                                    });
                                }
                            }
                        });
                    });
                }

                // Strategy 3: All news-related links
                if (items.length === 0) {
                    const allLinks = document.querySelectorAll('a[href*="finviz.com/news"], a[href*="bloomberg"], a[href*="reuters"], a[href*="cnbc"]');
                    console.log('Found all news links:', allLinks.length);

                    allLinks.forEach(link => {
                        const headline = link.textContent.trim();
                        if (headline.length > 10) {
                            items.push({
                                headline: headline,
                                url: link.href,
                                time: '',
                                source: link.hostname || ''
                            });
                        }
                    });
                }

                console.log('Total items extracted:', items.length);
                return items;
            }''')

            news_data = news_items
            print(f'Extracted {len(news_data)} news items')

            # If no data extracted from JS, try manual parsing
            if len(news_data) == 0:
                print('No news items found via JavaScript, checking page structure...')
                # Get all links on the page for debugging
                all_links = await page.query_selector_all('a')
                print(f'Total links on page: {len(all_links)}')

            # Step 7: Save extracted data
            print('Step 7: Saving extracted data...')

            # Save to JSON
            with open('/Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/finviz/raw/news_data.json', 'w') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'source': 'Finviz.com',
                    'total_items': len(news_data),
                    'news': news_data
                }, f, indent=2)

            print('News data saved to JSON')

            # Keep browser open for a moment to see the final state
            print('Keeping browser open for 5 seconds for verification...')
            await asyncio.sleep(5)

            # Close browser
            await browser.close()

            return news_data

        except Exception as e:
            print(f"Error occurred: {e}")
            import traceback
            traceback.print_exc()
            await take_screenshot_safe(page, "/Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/finviz/screenshots/error.png", "Error state")
            await browser.close()
            raise

async def main():
    news_data = await login_and_screenshot_finviz()
    print(f'\n=== SCRAPING COMPLETE ===')
    print(f'Total news items extracted: {len(news_data)}')
    print(f'\nScreenshots saved to: /Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/finviz/screenshots/')
    print(f'Raw data saved to: /Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/finviz/raw/news_data.json')
    return news_data

if __name__ == '__main__':
    asyncio.run(main())
