import json
from collections import Counter
from datetime import datetime
from urllib.parse import urlparse

# Load the news data
with open('/Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/finviz/raw/news_data.json', 'r') as f:
    data = json.load(f)

news_items = data['news']

# Filter out navigation links and get actual news
actual_news = [item for item in news_items if
               item['headline'] not in ['Elite Subscription', 'Feature Preview', 'Market News', 'Stocks News', 'Crypto News']
               and 'subscription' not in item['url'].lower()
               and 'feature_preview' not in item['url'].lower()]

# Get unique news items (deduplicate by headline)
seen_headlines = set()
unique_news = []
for item in actual_news:
    if item['headline'] not in seen_headlines:
        seen_headlines.add(item['headline'])
        unique_news.append(item)

# Count sources
sources = [urlparse(item['url']).netloc for item in unique_news]
source_counts = Counter(sources)

# Categorize news by topic (simple keyword matching)
categories = {
    'Federal Reserve & Interest Rates': [],
    'Stock Market & Indices': [],
    'Cryptocurrency': [],
    'Technology & AI': [],
    'Company Earnings & Performance': [],
    'Economic Data': [],
    'International Markets': [],
    'Energy & Commodities': [],
    'Real Estate': [],
    'Other': []
}

for item in unique_news:
    headline_lower = item['headline'].lower()

    if any(keyword in headline_lower for keyword in ['fed', 'rate cut', 'interest rate', 'federal reserve', 'powell', 'williams', 'collins']):
        categories['Federal Reserve & Interest Rates'].append(item)
    elif any(keyword in headline_lower for keyword in ['bitcoin', 'crypto', 'blockchain', 'cryptocurrency']):
        categories['Cryptocurrency'].append(item)
    elif any(keyword in headline_lower for keyword in ['nvidia', 'ai ', 'artificial intelligence', 'deepseek', 'tech giant', 'chip', 'semiconductor']):
        categories['Technology & AI'].append(item)
    elif any(keyword in headline_lower for keyword in ['dow', 's&p', 'nasdaq', 'stock market', 'stocks', 'indices', 'rally', 'selloff']):
        categories['Stock Market & Indices'].append(item)
    elif any(keyword in headline_lower for keyword in ['earnings', 'revenue', 'profit', 'loss', 'quarterly', 'guidance', 'forecast']):
        categories['Company Earnings & Performance'].append(item)
    elif any(keyword in headline_lower for keyword in ['gdp', 'inflation', 'employment', 'consumer', 'economic', 'business activity', 'pmi', 'sentiment']):
        categories['Economic Data'].append(item)
    elif any(keyword in headline_lower for keyword in ['china', 'europe', 'uk', 'global', 'asia', 'japan', 'germany', 'france']):
        categories['International Markets'].append(item)
    elif any(keyword in headline_lower for keyword in ['oil', 'energy', 'lng', 'gas', 'commodities', 'gold']):
        categories['Energy & Commodities'].append(item)
    elif any(keyword in headline_lower for keyword in ['housing', 'real estate', 'home', 'mortgage']):
        categories['Real Estate'].append(item)
    else:
        categories['Other'].append(item)

# Generate markdown report
report = f"""# Finviz Stock News Report

**Generated:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
**Source:** Finviz.com
**Total News Items Captured:** {len(unique_news)}
**Data Collection Time:** {data['timestamp']}

---

## Executive Summary

This report contains {len(unique_news)} unique stock market news headlines scraped from Finviz.com. The news covers major market movements, Federal Reserve policy updates, cryptocurrency volatility, technology sector developments, and global economic trends.

### Top News Sources

"""

# Add top sources
for source, count in source_counts.most_common(15):
    report += f"- **{source}**: {count} articles\n"

report += "\n---\n\n"

# Add categorized news
for category, items in categories.items():
    if items:
        report += f"## {category}\n\n"
        report += f"*{len(items)} headlines*\n\n"

        for item in items[:50]:  # Limit to 50 per category to keep report manageable
            report += f"### {item['headline']}\n\n"
            report += f"**Source:** {urlparse(item['url']).netloc}\n\n"
            report += f"**URL:** [{item['url']}]({item['url']})\n\n"
            if item.get('time'):
                report += f"**Time:** {item['time']}\n\n"
            report += "---\n\n"

# Add appendix with all headlines
report += "\n\n## Appendix: Complete Headlines List\n\n"
report += f"Total unique headlines: {len(unique_news)}\n\n"

for i, item in enumerate(unique_news, 1):
    report += f"{i}. {item['headline']}\n"

# Save report
with open('/Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/finviz/reports/finviz_news_report.md', 'w', encoding='utf-8') as f:
    f.write(report)

print(f"Report generated successfully!")
print(f"Total unique news items: {len(unique_news)}")
print(f"Report saved to: /Users/venkat/workfolder/playwright-min/outputs/stock_news_scraper/finviz/reports/finviz_news_report.md")
