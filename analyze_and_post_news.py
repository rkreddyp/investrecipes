#!/usr/bin/env python3
"""Comprehensive news analysis and Slack posting"""

import json
import requests
from datetime import datetime

# Slack configuration
import os
SLACK_TOKEN = os.getenv("SLACK_TOKEN", "your-slack-token-here")
CHANNEL = os.getenv("SLACK_CHANNEL", "stock_ops_dev")

# Load the news data
with open('/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/default/raw/headlines.json', 'r') as f:
    news_data = json.load(f)

def perform_comprehensive_analysis():
    """Analyze all news for trends, connections, and insights"""

    # Combine all articles
    all_articles = []
    for article in news_data.get('business_insider', []):
        all_articles.append({'headline': article['headline'], 'url': article['url'], 'source': 'Business Insider'})
    for article in news_data.get('forbes', []):
        all_articles.append({'headline': article['headline'], 'url': article['url'], 'source': 'Forbes'})

    analysis = {
        'total_stories': len(all_articles),
        'date': datetime.now().strftime('%B %d, %Y'),
        'major_themes': [],
        'key_insights': [],
        'market_implications': [],
        'notable_developments': [],
        'interconnections': []
    }

    # Major Theme 1: AI Revolution & Economic Impact
    ai_stories = [a for a in all_articles if any(kw in a['headline'].lower() for kw in ['ai', 'nvidia', 'openai', 'artificial intelligence'])]
    if ai_stories:
        analysis['major_themes'].append({
            'title': 'AI Revolution Reaches Critical Inflection Point',
            'count': len(ai_stories),
            'analysis': '''The AI sector dominates today's news cycle with multiple interconnected stories revealing both the technology's massive potential and emerging risks:

• **Nvidia Earnings as Market Bellwether**: Investor anxiety around Nvidia's Q3 results reflects broader concerns about AI infrastructure sustainability
• **OpenAI Governance Crisis**: Larry Summers' resignation over Epstein ties highlights ongoing governance challenges in AI leadership
• **AI Bubble Debate Intensifies**: Multiple stories question whether we're in an AI infrastructure boom or bubble
• **Trillion Dollar Borrowing Concerns**: Forbes reports AI companies' massive debt accumulation could trigger the next credit crunch
• **Search Revolution (GEO vs SEO)**: The shift from Search Engine Optimization to Generative Engine Optimization signals fundamental changes in how information is discovered

**Key Insight**: The AI sector is experiencing simultaneous euphoria and doubt - massive investment continues while serious questions emerge about sustainability, governance, and economic impact.''',
            'stories': ai_stories[:5]
        })

    # Major Theme 2: Corporate America Under Pressure
    retail_target = [a for a in all_articles if any(kw in a['headline'].lower() for kw in ['target', 'retail', 'walmart'])]
    inflation_biz = [a for a in all_articles if any(kw in a['headline'].lower() for kw in ['inflation', 'price hike', 'small business'])]
    workforce = [a for a in all_articles if any(kw in a['headline'].lower() for kw in ['hire', 'shipbuilder', 'navy', 'amazon', 'buc-ee'])]

    corporate_pressure_stories = retail_target + inflation_biz + workforce
    if corporate_pressure_stories:
        analysis['major_themes'].append({
            'title': 'Corporate America Faces Multi-Front Pressures',
            'count': len(corporate_pressure_stories),
            'analysis': '''American businesses are navigating a complex web of challenges across multiple fronts:

• **Retail Sector Struggles**: Target's disappointing earnings signal ongoing challenges heading into the critical holiday season, even as consumers seek value (Walmart's $4 Thanksgiving dinner)
• **Inflationary Pressures Persist**: Most small businesses planning price hikes as inflation continues to squeeze margins
• **Labor Market Competition**: Navy can't compete with Buc-ee's and Amazon wages for shipbuilders - a telling sign of how retail and logistics have disrupted traditional labor markets
• **Consumer Behavior Shifts**: Stories about $89 sweatshirts as status symbols suggest continued spending in certain categories despite broader economic concerns

**Key Insight**: The bifurcation of the American economy continues - discount retailers and luxury brands thrive while traditional mid-market players struggle.''',
            'stories': corporate_pressure_stories[:4]
        })

    # Major Theme 3: Tesla & Elon Musk Ecosystem
    tesla_stories = [a for a in all_articles if any(kw in a['headline'].lower() for kw in ['tesla', 'elon', 'musk', 'cybercab', 'robot'])]
    if tesla_stories:
        analysis['major_themes'].append({
            'title': 'Tesla & Musk Face Regulatory and Execution Challenges',
            'count': len(tesla_stories),
            'analysis': '''Multiple stories reveal challenges in Tesla's ambitious product roadmap:

• **Cybercab Legal Issues**: Tesla can't legally sell the promised Cybercab due to regulatory constraints
• **Robotics Showcase**: Tesla robots featured at Wall Street conferences, but questions remain about commercial viability

**Key Insight**: Gap between Musk's promises and regulatory/technical reality continues to widen, yet investor enthusiasm persists.''',
            'stories': tesla_stories
        })

    # Major Theme 4: Geopolitics & Business
    trump_saudi = [a for a in all_articles if any(kw in a['headline'].lower() for kw in ['trump', 'saudi', 'white house dinner'])]
    if trump_saudi:
        analysis['major_themes'].append({
            'title': 'Saudi-US Business Ties Deepen',
            'count': len(trump_saudi),
            'analysis': '''Multiple stories highlight the strengthening relationship between Saudi Arabia and American business interests:

• **White House Dinner**: Nearly 50 executives attended dinner for Saudi Crown Prince, signaling deep business ties
• **Trump's Financial Connections**: Forbes reports on Trump's Saudi financial ties and compensation for hosting Saudi-backed golf events

**Key Insight**: Saudi Arabia's economic diversification strategy (Vision 2030) increasingly intertwines with American corporate interests, regardless of political administration.''',
            'stories': trump_saudi
        })

    # Major Theme 5: Healthcare & Biotech Innovation
    healthcare = [a for a in all_articles if any(kw in a['headline'].lower() for kw in ['eli lilly', 'healthcare', 'cancer', 'biotech', 'drug', 'ai-powered cancer'])]
    if healthcare:
        analysis['major_themes'].append({
            'title': 'Healthcare Innovation & Investment Surge',
            'count': len(healthcare),
            'analysis': '''The healthcare and biotech sector shows significant activity:

• **Major Funding**: Former Eli Lilly exec raises $52M seed round for healthcare AI startup at $400M valuation
• **AI-Powered Therapeutics**: Korean biotech companies developing AI-powered cancer drugs, creating new billionaires
• **Strategic Partnerships**: Eli Lilly deals propelling biotech founders into billionaire ranks

**Key Insight**: AI convergence with healthcare creating massive value and attracting significant capital, despite broader market volatility.''',
            'stories': healthcare
        })

    # Market Implications
    analysis['market_implications'] = [
        {
            'title': 'AI Infrastructure Investment at Critical Juncture',
            'implication': 'Trillion-dollar AI borrowing combined with questions about bubble dynamics suggests potential for significant market volatility. Nvidia earnings will be closely watched as a key indicator.'
        },
        {
            'title': 'Consumer Discretionary Sector Divergence',
            'implication': 'Target struggles while luxury brands and discount retailers perform suggests continued K-shaped recovery. Holiday shopping season will be critical test.'
        },
        {
            'title': 'Labor Market Remains Tight Despite Fed Actions',
            'implication': 'Navy shipbuilder wage competition with retail indicates labor market strength persists, potentially keeping inflationary pressure elevated.'
        },
        {
            'title': 'Emerging Markets Creating Billionaires',
            'implication': 'Indian IPO boom and Korean biotech success show continued global wealth creation opportunities outside traditional US/European markets.'
        }
    ]

    # Key Interconnections
    analysis['interconnections'] = [
        {
            'theme': 'AI Everywhere',
            'connection': 'AI threads run through multiple stories: Nvidia hardware, OpenAI governance, healthcare AI startup, AI-powered cancer drugs, GEO replacing SEO, and Microsoft AI hiring. This isn\'t siloed tech news - AI is reshaping every sector simultaneously.'
        },
        {
            'theme': 'The Inflation-Labor-Retail Triangle',
            'connection': 'Target\'s struggles, small business price hikes, and Navy wage competition form interconnected story: tight labor markets drive wages up, forcing businesses to raise prices, squeezing retailers caught in the middle, especially those serving price-sensitive consumers.'
        },
        {
            'theme': 'Governance & Trust Crisis',
            'connection': 'Larry Summers/OpenAI resignation and Trump\'s various business entanglements highlight ongoing questions about governance, conflicts of interest, and trust in leadership across both tech and politics.'
        }
    ]

    # Notable Developments
    analysis['notable_developments'] = [
        'IPO boom in India minting new billionaires - global wealth creation shifting eastward',
        'Wealthfront entering mortgage market - fintech disruption expanding beyond core products',
        'Employee wellbeing and caregiving support emerging as business imperatives (multiple Forbes stories)',
        'Markets showing volatility on Fed signals and earnings crosscurrents - uncertainty remains high'
    ]

    return analysis

def create_analysis_message(analysis):
    """Create Slack message blocks for comprehensive analysis"""
    blocks = []

    # Header
    blocks.append({
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": f"📊 Deep Dive: Business News Analysis - {analysis['date']}"
        }
    })

    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"*Comprehensive analysis of {analysis['total_stories']} stories from Business Insider & Forbes*"
        }
    })

    blocks.append({"type": "divider"})

    # Executive Summary
    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*📌 Executive Summary*\n\nToday's news reveals an economy at multiple crossroads: AI investment reaching potentially unsustainable levels, corporate America squeezed by persistent inflation and labor costs, and significant shifts in global economic power. The common thread: transformation and uncertainty across every major sector."
        }
    })

    blocks.append({"type": "divider"})

    # Major themes will be posted as thread replies
    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"*🔍 Major Themes Identified*\n\n{len(analysis['major_themes'])} deep-dive analyses in thread below ⬇️"
        }
    })

    blocks.append({"type": "divider"})

    # Market Implications Summary
    impl_text = "*💹 Market Implications*\n\n"
    for impl in analysis['market_implications']:
        impl_text += f"• *{impl['title']}*\n  {impl['implication']}\n\n"

    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": impl_text
        }
    })

    blocks.append({"type": "divider"})

    # Key Interconnections
    conn_text = "*🔗 Key Interconnections*\n\n"
    for conn in analysis['interconnections']:
        conn_text += f"• *{conn['theme']}*: {conn['connection']}\n\n"

    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": conn_text
        }
    })

    blocks.append({"type": "divider"})

    # Notable Developments
    notable_text = "*⚡ Notable Developments*\n\n"
    for dev in analysis['notable_developments']:
        notable_text += f"• {dev}\n"

    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": notable_text
        }
    })

    # Footer
    blocks.append({"type": "divider"})
    blocks.append({
        "type": "context",
        "elements": [{
            "type": "mrkdwn",
            "text": "🧵 _Detailed theme analyses with supporting stories in thread_ | 📁 Raw data: outputs/business_news_scraper/default/"
        }]
    })

    return blocks

def create_theme_message(theme):
    """Create detailed theme analysis message"""
    blocks = []

    blocks.append({
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": f"🔎 {theme['title']}"
        }
    })

    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"*Analysis of {theme['count']} related stories:*"
        }
    })

    blocks.append({"type": "divider"})

    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": theme['analysis']
        }
    })

    blocks.append({"type": "divider"})

    # Supporting stories
    if theme.get('stories'):
        stories_text = "*📰 Supporting Stories:*\n\n"
        for i, story in enumerate(theme['stories'], 1):
            stories_text += f"{i}. <{story['url']}|{story['headline']}>\n   _{story['source']}_\n\n"

        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": stories_text
            }
        })

    return blocks

def post_analysis_to_slack():
    """Post comprehensive analysis to Slack"""
    analysis = perform_comprehensive_analysis()

    headers = {
        "Authorization": f"Bearer {SLACK_TOKEN}",
        "Content-Type": "application/json"
    }

    # Post main analysis message
    main_blocks = create_analysis_message(analysis)
    main_payload = {
        "channel": CHANNEL,
        "blocks": main_blocks,
        "text": f"Deep Dive: Business News Analysis - {analysis['date']}"
    }

    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers=headers,
        json=main_payload
    )

    main_result = response.json()

    if not main_result.get("ok"):
        print(f"❌ Error posting analysis: {main_result.get('error')}")
        return main_result

    print(f"✅ Posted main analysis to #{CHANNEL}")
    thread_ts = main_result.get("ts")

    # Post detailed theme analyses as thread replies
    for theme in analysis['major_themes']:
        theme_blocks = create_theme_message(theme)

        thread_payload = {
            "channel": CHANNEL,
            "thread_ts": thread_ts,
            "blocks": theme_blocks,
            "text": theme['title']
        }

        response = requests.post(
            "https://slack.com/api/chat.postMessage",
            headers=headers,
            json=thread_payload
        )

        result = response.json()
        if result.get("ok"):
            print(f"  ✅ Posted theme: {theme['title']}")
        else:
            print(f"  ❌ Error posting theme: {result.get('error')}")

    print(f"\n🎉 Analysis complete with {len(analysis['major_themes'])} theme deep-dives")
    return main_result

if __name__ == "__main__":
    result = post_analysis_to_slack()
