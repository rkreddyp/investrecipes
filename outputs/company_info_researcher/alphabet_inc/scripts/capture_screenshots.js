const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  try {
    // Capture Alphabet official website
    console.log('Navigating to abc.xyz...');
    await page.goto('https://abc.xyz/', { waitUntil: 'networkidle', timeout: 30000 });
    await page.screenshot({
      path: '/Users/venkat/workfolder/playwright-min/outputs/company_info_researcher/alphabet_inc/screenshots/alphabet_official_website.png',
      fullPage: true
    });
    console.log('Screenshot saved: alphabet_official_website.png');

    // Capture Yahoo Finance
    console.log('Navigating to Yahoo Finance...');
    await page.goto('https://finance.yahoo.com/quote/GOOGL/', { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(2000); // Wait for dynamic content
    await page.screenshot({
      path: '/Users/venkat/workfolder/playwright-min/outputs/company_info_researcher/alphabet_inc/screenshots/yahoo_finance_googl.png',
      fullPage: true
    });
    console.log('Screenshot saved: yahoo_finance_googl.png');

    // Capture Google About page
    console.log('Navigating to about.google...');
    await page.goto('https://about.google/', { waitUntil: 'networkidle', timeout: 30000 });
    await page.screenshot({
      path: '/Users/venkat/workfolder/playwright-min/outputs/company_info_researcher/alphabet_inc/screenshots/google_about.png',
      fullPage: true
    });
    console.log('Screenshot saved: google_about.png');

    // Capture Yahoo Finance Profile tab
    console.log('Navigating to Yahoo Finance Profile...');
    await page.goto('https://finance.yahoo.com/quote/GOOGL/profile/', { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(2000);
    await page.screenshot({
      path: '/Users/venkat/workfolder/playwright-min/outputs/company_info_researcher/alphabet_inc/screenshots/yahoo_finance_profile.png',
      fullPage: true
    });
    console.log('Screenshot saved: yahoo_finance_profile.png');

  } catch (error) {
    console.error('Error:', error);
  } finally {
    await browser.close();
    console.log('Browser closed successfully');
  }
})();
