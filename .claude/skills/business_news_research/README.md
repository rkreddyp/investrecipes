# Business News Research Skill

## Overview
Multi-agent orchestration system that scrapes headlines from 15 top business news websites in parallel to create comprehensive daily business news digests.

## How It Works

### Lead Coordinator Pattern
The `SKILL.md` acts as a **News Research Coordinator** that:
- Orchestrates 5 specialized news scraper agents in PARALLEL
- Launches 1 report writer agent SEQUENTIALLY after scraping completes
- Never scrapes news itself
- Keeps all responses SHORT (2-3 sentences max)
- Delegates ALL work to specialized scraper agents

### Specialized News Scraper Agents (from `.claude/agents/`)

#### Parallel Scraper Agents (Run Simultaneously)
1. **Financial News Scraper** - Bloomberg, Reuters, Financial Times
2. **Market News Scraper** - CNBC, MarketWatch, Yahoo Finance
3. **Business News Scraper** - WSJ, Business Insider, Forbes
4. **Tech News Scraper** - TechCrunch, The Verge, Ars Technica
5. **Industry News Scraper** - Barron's, Fortune, The Economist

#### Sequential Report Agent (Runs After Scraping)
6. **News Report Writer** - Synthesizes all headlines into daily digest

## 15 Top Business News Websites

### Financial News (3 sites)
1. **Bloomberg** (bloomberg.com)
   - Global financial news leader
   - Markets, economics, technology, politics

2. **Reuters Business** (reuters.com/business)
   - Breaking business news
   - International coverage

3. **Financial Times** (ft.com)
   - Global business journalism
   - Markets and economics

### Market News (3 sites)
4. **CNBC** (cnbc.com)
   - Real-time market news
   - Stock quotes and analysis

5. **MarketWatch** (marketwatch.com)
   - Market data and financial information
   - Investment tools and stock picks

6. **Yahoo Finance** (finance.yahoo.com/news)
   - Business and financial news
   - Stock market coverage

### Business News (3 sites)
7. **Wall Street Journal** (wsj.com)
   - Business and economic news
   - In-depth reporting

8. **Business Insider** (businessinsider.com)
   - Business, tech, finance news
   - Markets and strategy

9. **Forbes** (forbes.com)
   - Business, investing, technology
   - Entrepreneurship and leadership

### Tech Business News (3 sites)
10. **TechCrunch** (techcrunch.com)
    - Technology and startup news
    - Venture capital and funding

11. **The Verge** (theverge.com)
    - Technology news and reviews
    - Science and culture

12. **Ars Technica** (arstechnica.com)
    - Technology news and analysis
    - Science and policy

### Industry News (3 sites)
13. **Barron's** (barrons.com)
    - Investment news and analysis
    - Market commentary

14. **Fortune** (fortune.com)
    - Business news and analysis
    - Fortune 500 coverage

15. **The Economist** (economist.com/business)
    - Global business coverage
    - Economic analysis

## Usage

### Simple Request
```
"Get today's business news"
"Scrape latest business headlines"
"What's happening in business news today?"
```

### Coordinator Response
The coordinator will:
1. Launch all 5 scraper agents in parallel
2. Each agent scrapes 3 websites (10 headlines each)
3. Wait for scraping to complete (~5 minutes)
4. Launch report writer to synthesize findings
5. Upload daily digest to S3
6. Provide S3 key for download

### Example Interaction
```
User: "Get today's business news"

Coordinator: "Launching parallel news scraping across 15 sources. Deploying 5 scraper agents."

[5 agents scrape simultaneously...]

Coordinator: "Scraping complete. Compiling news digest."

[Report writer synthesizes all headlines...]

Coordinator: "Report uploaded: business_news_digest_20241116.md"
```

## News Digest Contents

### Executive Summary
- 3-4 paragraph overview of top stories
- Major developments across all sources

### Trending Topics
- Topics mentioned across multiple sources
- Related companies and industries
- Significance and impact

### Top Stories by Category
- Markets & Trading
- Corporate News
- Technology
- Economic Policy
- International Business

### All Headlines by Source
- ~150 total headlines
- Organized by news source
- Dates, summaries, and links

### Key Companies Mentioned
- Most frequently mentioned companies
- Number of mentions per company

### Source Links
- All 15 website URLs
- Direct links to sources

## Advantages of Parallel Architecture

### Time Efficiency
- **Sequential:** ~25 minutes (5 scrapers × 5 min each)
- **Parallel:** ~5 minutes (all scrapers run simultaneously)
- **80% time reduction**

### Comprehensive Coverage
- 15 top business news websites
- ~150 total headlines
- Multiple perspectives on same stories
- Trending topic identification

### Categorization
- Financial news
- Market news
- General business
- Tech business
- Industry-specific

## Configuration

### Coordinator Settings
```yaml
max_turns: 3        # Quick orchestration only
max_budget: 0.05    # Low cost (just coordination)
thinking_budget: 5000  # Minimal thinking needed
```

### Scraper Agent Settings
```yaml
max_turns: 5        # Enough for browsing 3 sites
max_budget: 0.10    # Reasonable scraping budget
thinking_budget: 10000  # Content extraction capability
```

### Report Writer Settings
```yaml
max_turns: 3        # Synthesis only
max_budget: 0.05    # Report writing only
thinking_budget: 10000  # Thoughtful synthesis
```

## Output

### File Format
```
/tmp/business_news_digest_{YYYYMMDD}.md
```

### S3 Upload
Automatically uploaded to:
```
https://transilience--s3-file-upload-fastapi-app-dev.modal.run/upload_s3
```

### User Receives
- S3 key for download
- Comprehensive news digest
- ~150 headlines synthesized
- Trending topics identified

## Use Cases

### Daily News Monitoring
- Get comprehensive daily business news
- Monitor trending business topics
- Track company mentions

### Market Research
- Stay updated on market developments
- Track industry news
- Monitor competitor news

### Competitive Intelligence
- Track company announcements
- Monitor industry trends
- Identify emerging topics

### Content Curation
- Aggregate news from multiple sources
- Identify trending stories
- Curate daily briefings

## Success Metrics

A successful news scraping session:
- ✅ All 5 scraper agents complete successfully
- ✅ Each agent provides 30 headlines (10 per site)
- ✅ Total ~150 headlines collected
- ✅ Report writer synthesizes all headlines
- ✅ Trending topics identified
- ✅ Final digest is comprehensive
- ✅ Digest uploaded to S3 successfully
- ✅ User receives S3 key
- ✅ Total time < 10 minutes
- ✅ All responses kept short (2-3 sentences)

## Best Practices

### For Users
- ✅ Run once daily for comprehensive coverage
- ✅ Specify time period if needed (today, this week)
- ✅ Can filter by category if desired

### For Coordinator
- ✅ Launch all scraper agents in PARALLEL
- ✅ Keep responses SHORT (2-3 sentences)
- ✅ Never scrape news yourself
- ✅ Wait for all agents before report synthesis

### For Scraper Agents
- ✅ Focus on your 3 designated websites
- ✅ Extract 10 headlines per site
- ✅ Include date, headline, summary, URL
- ✅ Return only findings (no greetings)

## Future Enhancements

Potential additional scrapers:
- Cryptocurrency news (CoinDesk, Cointelegraph)
- Real estate news (Real Estate Weekly, CoStar)
- Energy news (Oil Price, Energy Voice)
- Healthcare news (Healthcare Dive, FierceHealthcare)
- Retail news (Retail Dive, Chain Store Age)
- International editions (UK, Asia, EU sources)

