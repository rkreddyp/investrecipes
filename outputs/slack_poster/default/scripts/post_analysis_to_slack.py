#!/usr/bin/env python3
"""
Post comprehensive news analysis to Slack with topic-based threading
"""

import requests
import json
from datetime import datetime

# Slack configuration
import os
SLACK_TOKEN = os.getenv("SLACK_TOKEN", "your-slack-token-here")
CHANNEL = os.getenv("SLACK_CHANNEL", "stock_ops_dev")
SLACK_API_URL = "https://slack.com/api/chat.postMessage"

def post_to_slack(text, blocks=None, thread_ts=None):
    """Post a message to Slack"""
    headers = {
        "Authorization": f"Bearer {SLACK_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "channel": CHANNEL,
        "text": text
    }

    if blocks:
        payload["blocks"] = blocks

    if thread_ts:
        payload["thread_ts"] = thread_ts

    response = requests.post(SLACK_API_URL, headers=headers, json=payload)
    return response.json()

def create_main_summary():
    """Create main summary message with topic breakdown"""

    summary_text = """📰 *Market & Economic Analysis Report - November 21, 2025*

*221 headlines analyzed* from Business Insider, Forbes, and Finviz (aggregating Bloomberg, Reuters, CNBC, MarketWatch, Yahoo Finance, WSJ, NYT, and others)

🔍 *Executive Summary:*
Markets experienced extreme volatility - the wildest trading day since April's tariff shock. Three major narratives converged:
• AI sector correction despite strong Nvidia earnings
• Bitcoin crash below $82K (worst month since 2022)
• Mixed Fed signals creating rate-cut whiplash

📊 *Analysis organized into 4 major topics:*
1️⃣ *Market Volatility & Trends* - Peak warnings, dip-buying tests, extreme swings
2️⃣ *Economic Indicators* - Services strong/manufacturing weak, labor softening, inflation concerns
3️⃣ *Stock Market Deep Dive* - AI bubble fears, crypto meltdown, tech selloff
4️⃣ *Key Uncertainties* - Fed policy direction, AI investment returns, fund flow contradictions

💡 *Big Picture Insight:*
The convergence of AI valuation questions, crypto instability, and Fed uncertainty has created a critical inflection point. Dip-buying strategies face their most serious test, while retail-institutional sentiment divergence raises red flags.

_Full analysis with inline citations in threads below ⬇️_"""

    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "📰 Market & Economic Analysis Report",
                "emoji": True
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*November 21, 2025*\n221 headlines analyzed from 15+ top business sources"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*🔍 Executive Summary:*\nMarkets experienced extreme volatility - the *wildest trading day since April's tariff shock*. Three major narratives converged:\n• AI sector correction despite strong Nvidia earnings\n• Bitcoin crash below $82K (worst month since 2022)\n• Mixed Fed signals creating rate-cut whiplash"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*📊 Analysis Topics:*\n1️⃣ Market Volatility & Trends\n2️⃣ Economic Indicators\n3️⃣ Stock Market Deep Dive\n4️⃣ Key Uncertainties"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*💡 Big Picture:*\nThe convergence of AI valuation questions, crypto instability, and Fed uncertainty has created a critical inflection point. Dip-buying strategies face their most serious test."
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "📎 Full analysis with citations in threads below"
                }
            ]
        }
    ]

    return summary_text, blocks

def create_market_volatility_thread():
    """Topic 1: Market Volatility & Trends"""

    text = """*1️⃣ MARKET VOLATILITY & TRENDS*

*🔥 Extreme Market Volatility*
Markets experiencing most volatile period since April 2025 tariff shock. Bloomberg calls it the "wildest trading day" with roller-coaster conditions reflecting deep uncertainty across equities, crypto, and bonds. Amazon wiped out entire 2025 gains.

📊 _Sources: Bloomberg, Yahoo Finance, Reuters, MarketWatch_
🔗 https://www.bloomberg.com/news/articles/2025-11-21/wildest-trading-day-since-tariff-shock-to-test-dip-buyers-nerve

*⚠️ Market Peak Warnings*
Veteran strategist publicly calls market top, predicting 3-year downturn. Technical indicators show "indices shift net bearish" - but contradicted by US equity funds attracting 5th straight weekly inflow and global funds drawing 9th consecutive week of inflows.

📊 _Sources: MarketWatch, Mish Talk, Reuters_
🔗 https://www.marketwatch.com/bulletins/redirect/go?g=3bac8586-825a-475d-8f71-e7f187285c5e

*📉 Dip-Buying Under Severe Test*
Traditional "buy-the-dip" strategy facing most serious challenge. Even bullish strategist Tom Lee adjusting positioning. Nvidia's strong earnings met with "sell the news" - positive fundamentals failing to support prices, classic warning of psychology shift from buying dips to selling rallies.

📊 _Sources: Bloomberg, MarketWatch, Howard Lindzon, Mish Talk_
🔗 https://www.howardlindzon.com/p/you-can-only-disrespect-the-markets-for-so-long

*Confidence: HIGH* - Multiple independent sources confirm extraordinary volatility and market stress"""

    return text

def create_economic_indicators_thread():
    """Topic 2: Economic Indicators"""

    text = """*2️⃣ ECONOMIC INDICATORS*

*📊 Services Strong, Manufacturing Weak*
Clear economic bifurcation: US business activity expands at fastest pace in 4 months driven by services, while manufacturing struggles. Pattern extends globally - Euro-Zone and France show same dynamic. Creates two-speed economy complicating Fed policy.

📊 _Sources: Bloomberg (3 articles), ZeroHedge_
🔗 https://www.bloomberg.com/news/articles/2025-11-21/us-business-activity-expands-at-fastest-pace-in-four-months

*👷 Labor Market Gradually Softening*
September: 119K jobs added, unemployment rises to 4.4%. Below pace needed to keep up with labor force growth. Weekly claims at 220K suggest no collapse, but trend shows hiring "rebounded in September, but the trend is still weakening."

📊 _Sources: Mish Talk, Calculated Risk Blog, Capital Spectator_
🔗 https://mishtalk.com/economics/september-jobs-up-119000-unemployment-rises-to-4-4-percent/

*📈 Inflation Concerns Resurface*
Wall Street rethinking inflation risks. FOMC minutes reveal inflation concerns causing Fed rate cut odds to plunge. Problem: CBO lowers tariff fiscal savings estimate by $1 trillion - tariffs won't offset spending as hoped, keeping fiscal stimulus and inflation pressures elevated.

📊 _Sources: Capital Spectator, Mish Talk, Forbes_
🔗 https://www.capitalspectator.com/is-wall-street-starting-to-rethink-inflation-risk/

*💰 AI Capex Masking Economic Weakness*
Massive corporate spending on AI infrastructure artificially inflating economic indicators. When tech giants flood bond markets with AI debt, it creates measured activity in business investment and construction - but if spending doesn't generate returns, economic strength is overstated.

📊 _Sources: Real Investment Advice, Reuters, Seeking Alpha_
🔗 https://realinvestmentadvice.com/resources/blog/capex-spending-on-ai-is-masking-economic-weakness/

*🏛️ Fed Policy Whiplash*
Contradictory Fed signals amplifying volatility: NY Fed's Williams calls for rate cut → markets rally. Boston Fed's Collins says rates "appropriate for now" → markets reverse. FOMC minutes show inflation concerns. Markets uncertain whether December brings cut or pause.

📊 _Sources: MarketWatch, NYT, Bloomberg (2), CNBC, ZeroHedge, Capital Spectator_
🔗 https://www.nytimes.com/2025/11/21/business/fed-interest-rates-inflation-jobs.html

*Confidence: HIGH* - Official government data and Federal Reserve communications confirm these trends"""

    return text

def create_stock_market_thread():
    """Topic 3: Stock Market Deep Dive"""

    text = """*3️⃣ STOCK MARKET DEEP DIVE*

*🤖 AI Sector Correction Despite Strong Fundamentals*
Nvidia "crushed its quarter" but CEO Jensen Huang said in leaked all-hands "the market did not appreciate it." Classic "sell the news" event. Wall Street vs Main Street divergence: institutions exiting while retail stays bullish. Questions mounting: "Should You Fear The AI Bubble?" and "Is Today's AI Cycle A Repeat Of The Metaverse Overbuild?"

📊 _Sources: Business Insider, Yahoo Finance, Mish Talk, Reuters, CNBC, Seeking Alpha (2)_
🔗 https://www.businessinsider.com/jensen-huang-market-nvidia-quarter-meeting-2025-11
🔗 https://finance.yahoo.com/news/wall-street-doesnt-agree-with-main-street-about-nvidia-110044035.html

*₿ Cryptocurrency Severe Distress*
Bitcoin heading for *worst month since crypto collapse of 2022*. Flash crashed below $82K, threatening $80K break. Forbes reveals "Inside The Bitcoin Meltdown: How Two Big Institutions Triggered The Crash." Broad crypto rout - "cryptocurrencies whipped by flight from risk." Robinhood shares brutal weekly loss as crypto/AI hit hard.

📊 _Sources: CNBC, Yahoo Finance, Reuters, ZeroHedge (2), Forbes (2), Howard Lindzon, Real Investment Advice_
🔗 https://www.cnbc.com/2025/11/21/bitcoin-continues-slide-thats-roiling-markets-threatens-to-break-below-80000.html
🔗 https://finance.yahoo.com/news/bitcoin-heading-worst-month-since-075033170.html
🔗 https://www.forbes.com/sites/greatspeculations/2025/11/21/inside-the-bitcoin-meltdown-how-two-big-institutions-triggered-the-crash/

*💻 Major Tech Stocks Declining*
Amazon's entire 2025 year-to-date gain wiped out. AMD crashing - Forbes asks "Should You Buy More?" European/UK shares fall on global tech rout. Paradox: BofA says "Tech stocks still set for record $75 billion inflow in 2025" - suggesting fund flows are lagging indicator or retail buying while institutions exit.

📊 _Sources: MarketWatch, Forbes, Reuters (3)_
🔗 https://www.marketwatch.com/bulletins/redirect/go?g=0d64cef8-37a8-4658-a3e5-782c6ddf4bc4
🔗 https://www.forbes.com/sites/greatspeculations/2025/11/21/as-amd-stock-crashes-should-you-buy-more/

*😰 Diverging Retail vs Institutional Sentiment*
Dangerous sentiment gap: retail remains bullish while institutions exit. "Wall Street doesn't agree with Main Street about Nvidia" crystallizes this divide. Pattern mirrors crypto where retail slow to react to worst month since 2022. Historical precedent: retail-institutional divergence often presages further declines as retail eventually capitulates.

📊 _Sources: Yahoo Finance (2), Reuters, Business Insider_
🔗 https://finance.yahoo.com/news/wall-street-doesnt-agree-with-main-street-about-nvidia-110044035.html

*Confidence: HIGH* - Specific company examples, quantifiable losses, explicit CEO commentary, broad sector reporting"""

    return text

def create_uncertainties_thread():
    """Topic 4: Key Uncertainties & Contradictions"""

    text = """*4️⃣ KEY UNCERTAINTIES & CONTRADICTIONS*

*❓ Fund Flows vs Price Action Paradox*
CONTRADICTION: Equities attracting 5th straight weekly inflow, global funds 9th consecutive week, tech set for record $75B inflow in 2025 (BofA)... YET prices declining sharply with Amazon wiping 2025 gains and broad selloffs.

Possible explanations:
• Fund flows are lagging indicator - institutions quietly exiting
• Money coming in is retail while institutional money exits
• Selling pressure (margin calls, algo trading, options hedging) overwhelming positive flows

📊 _Sources: Reuters (3), MarketWatch, Business Insider_
🔗 https://www.reuters.com/business/us-equity-funds-attract-fifth-straight-weekly-inflow-amid-robust-earnings-2025-11-21/
🔗 https://www.reuters.com/business/global-markets-flows-bofa-urgent-2025-11-21/

*🏛️ Fed Policy Direction Unclear*
Most significant market uncertainty. Contradictory signals: Williams wants cuts, Collins says rates appropriate, FOMC minutes show inflation worries. Markets could rally on dovish OR sell on hawkish with no clear resolution. Rate cut odds fluctuating wildly based on lack of data during Thanksgiving week.

📊 _Sources: Multiple Fed official statements, FOMC minutes, market commentary_

*🤖 AI Investment Return Timeline Ambiguous*
While AI concerns rising, actual return timelines unclear. Nvidia posting strong current earnings yet market selling. Question: Will AI deliver transformative returns or prove costly detour? TIMING is the problem - may eventually deliver but over longer period than markets pricing, or may never deliver adequate returns. Makes valuation nearly impossible.

📊 _Sources: Business Insider, Seeking Alpha (2), Real Investment Advice, Reuters_

*⚡ Cross-Cutting Themes:*
1. *AI Investment Sustainability* - Affects markets (stock corrections), economy (capex masking weakness), investor behavior (bubble concerns)
2. *Rate Cut Uncertainty Amplifier* - Unclear Fed path removes stable anchor for pricing risk, amplifies all other concerns
3. *Bubble Psychology Taking Hold* - Bubble framing appearing in mainstream financial media across AI, crypto, and broader equities

*Confidence: MEDIUM-HIGH* - Contradictions well-documented but resolution uncertain"""

    return text

def main():
    print("=" * 60)
    print("POSTING NEWS ANALYSIS TO SLACK")
    print("=" * 60)

    # Post main summary
    print("\n1. Posting main summary message...")
    summary_text, summary_blocks = create_main_summary()
    main_response = post_to_slack(summary_text, blocks=summary_blocks)

    if not main_response.get("ok"):
        print(f"❌ Error posting main message: {main_response.get('error')}")
        return

    thread_ts = main_response.get("ts")
    print(f"✅ Main message posted (ts: {thread_ts})")

    # Post topic threads
    topics = [
        ("Market Volatility & Trends", create_market_volatility_thread),
        ("Economic Indicators", create_economic_indicators_thread),
        ("Stock Market Deep Dive", create_stock_market_thread),
        ("Key Uncertainties", create_uncertainties_thread)
    ]

    for i, (topic_name, topic_func) in enumerate(topics, 2):
        print(f"\n{i}. Posting thread: {topic_name}...")
        thread_text = topic_func()
        thread_response = post_to_slack(thread_text, thread_ts=thread_ts)

        if thread_response.get("ok"):
            print(f"✅ Thread posted: {topic_name}")
        else:
            print(f"❌ Error posting thread: {thread_response.get('error')}")

    print("\n" + "=" * 60)
    print("✅ COMPLETE - News analysis posted to Slack!")
    print(f"📱 Channel: #{CHANNEL}")
    print(f"📊 221 headlines analyzed from 15+ sources")
    print(f"🧵 4 detailed topic threads created")
    print("=" * 60)

if __name__ == "__main__":
    main()
