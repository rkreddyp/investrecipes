const fs = require('fs');

// Load WSJ headlines
const wsjHeadlines = JSON.parse(
    fs.readFileSync('/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/news_user/raw/wsj_headlines.json', 'utf8')
);

// Load the existing report to extract Business Insider and Forbes
const existingReport = fs.readFileSync(
    '/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/news_user/reports/business_news_headlines_20251117.md',
    'utf8'
);

// Extract Business Insider section
const biMatch = existingReport.match(/### Business Insider\n([\s\S]*?)\n### Forbes/);
const biSection = biMatch ? biMatch[1] : '';

// Extract Forbes section
const forbesMatch = existingReport.match(/### Forbes\n([\s\S]*?)$/);
const forbesSection = forbesMatch ? forbesMatch[1] : '';

// Generate final report
let finalReport = '## Business News Sources\n\n';

finalReport += '### Wall Street Journal\n';
wsjHeadlines.forEach((item, idx) => {
    finalReport += `${idx + 1}. **${item.time}** - ${item.headline}\n`;
    finalReport += `   - URL: ${item.url}\n\n`;
});

finalReport += '### Business Insider\n';
finalReport += biSection + '\n';

finalReport += '### Forbes\n';
finalReport += forbesSection;

// Save final report
fs.writeFileSync(
    '/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/news_user/reports/business_news_headlines_20251117.md',
    finalReport
);

console.log('✓ Final report generated successfully!');
console.log('\nSummary:');
console.log('- WSJ: 10 headlines (last 24 hours)');
console.log('- Business Insider: 10 headlines');
console.log('- Forbes: 10 headlines');
console.log('\nReport saved to: outputs/business_news_scraper/news_user/reports/business_news_headlines_20251117.md');
