#!/usr/bin/env python3
"""Post insightful business news analysis to Twitter as a thread"""

import tweepy
import json
import time
from datetime import datetime

# Twitter API credentials
API_KEY = "9dy6mWFQawkymxqVQZs33JAp"
API_SECRET = "Et5gfF2mWcTg5S227kLtcXmMo8Qn6eF88x3xVf7xPQdH8RGgVB"
ACCESS_TOKEN = "1088426905634779136-hJvxovyNrsnmeNbVK4N7fhNppVHHrK"
ACCESS_TOKEN_SECRET = "E4F8fpaufTRNJwqKFx76a3ljRTPkpK3mS7f18KOqpwJ7FuA"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAALL3wQEAAAAABbyeVZaBQw%2BNs7pJPcfFOXdbYA0%3DDX9JaqUG0O5vC2celhwLBwwwY0Vplk5uEmjmVBLlRhuOwjeSwi"

# Load the news data
with open('/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/default/raw/headlines.json', 'r') as f:
    news_data = json.load(f)

def create_insightful_thread():
    """
    Create an insightful, educational thread about today's business news.
    Following best practices: Hook → Context → Insights → Implications
    """

    # Count articles
    bi_count = len(news_data.get('business_insider', []))
    forbes_count = len(news_data.get('forbes', []))
    total = bi_count + forbes_count

    tweets = []

    # Tweet 1: Hook - Clear, compelling overview
    tweets.append(
        f"📊 Business News Analysis - {datetime.now().strftime('%b %d, %Y')} 🧵\n\n"
        f"Analyzed {total} stories from BI & Forbes. Today reveals an economy at multiple crossroads:\n\n"
        "• AI investment hits inflection point\n"
        "• Corporate America under pressure\n"
        "• Geopolitics reshaping business\n\n"
        "Key insights below 👇"
    )

    # Tweet 2: Big Picture Context
    tweets.append(
        "🔍 The Big Picture:\n\n"
        "Today's news isn't about isolated events - it's about simultaneous transformation across every major sector. "
        "Three meta-trends are colliding: AI revolution, persistent inflation, and shifting global power dynamics."
    )

    # Tweet 3: AI Revolution Theme
    tweets.append(
        "🤖 AI Revolution at Inflection Point:\n\n"
        "19 stories touch on AI, revealing both euphoria & doubt:\n\n"
        "• Nvidia earnings = market bellwether\n"
        "• OpenAI governance crisis (Summers resigns)\n"
        "• Trillion $ AI borrowing could trigger credit crunch\n"
        "• AI bubble debate intensifies"
    )

    # Tweet 4: AI Deep Insight
    tweets.append(
        "Why AI matters now:\n\n"
        "The sector is experiencing simultaneous massive investment AND serious questions about sustainability. "
        "This isn't normal tech adoption - it's infrastructure-level transformation with infrastructure-level risks."
    )

    # Tweet 5: Corporate Pressure Theme
    tweets.append(
        "💼 Corporate America Squeezed:\n\n"
        "Multiple pressure points emerging:\n\n"
        "• Target's struggles heading into holidays\n"
        "• Small businesses planning price hikes\n"
        "• Navy can't compete with Buc-ee's wages (!)\n\n"
        "The story: Mid-market getting crushed between discount & luxury."
    )

    # Tweet 6: Labor Market Insight
    tweets.append(
        "🏗️ That Navy-Buc-ee's comparison is telling:\n\n"
        "When military shipbuilding can't compete with convenience store wages, it signals:\n"
        "1) Labor market strength persists\n"
        "2) Retail/logistics disrupted traditional wage structures\n"
        "3) Inflation pressure stays elevated"
    )

    # Tweet 7: Geopolitics Theme
    tweets.append(
        "🌍 Geopolitics Reshaping Business:\n\n"
        "• White House dinner: 50 execs meet Saudi Crown Prince\n"
        "• Forbes details Trump-Saudi financial ties\n"
        "• Indian IPO boom minting billionaires\n"
        "• Korean biotech deals creating wealth\n\n"
        "Power & capital are redistributing globally."
    )

    # Tweet 8: Healthcare/Innovation
    tweets.append(
        "🏥 Healthcare + AI = Massive Value Creation:\n\n"
        "$52M seed round for healthcare AI startup (ex-Eli Lilly exec)\n"
        "AI-powered cancer drugs creating new billionaires\n\n"
        "Despite market volatility, AI convergence with healthcare attracts significant capital."
    )

    # Tweet 9: Key Interconnections
    tweets.append(
        "🔗 Key Interconnection:\n\n"
        "The inflation-labor-retail triangle:\n\n"
        "Tight labor → wages up → businesses raise prices → retailers squeezed (especially mid-market)\n\n"
        "This explains Target's struggles while discount (Walmart) and luxury brands thrive."
    )

    # Tweet 10: Tesla/Musk Regulatory Reality
    tweets.append(
        "⚡ Tesla Reality Check:\n\n"
        "• Cybercab can't be legally sold as promised\n"
        "• Robot showcase raises viability questions\n\n"
        "Gap between Musk's promises and regulatory/technical reality continues widening. Investor enthusiasm persists anyway."
    )

    # Tweet 11: Market Implications
    tweets.append(
        "💹 Market Implications:\n\n"
        "1) AI infrastructure at critical juncture - Nvidia earnings crucial\n"
        "2) K-shaped recovery continues - avoid mid-market exposure\n"
        "3) Labor market strength = persistent inflation\n"
        "4) Emerging markets creating opportunities"
    )

    # Tweet 12: What to Watch
    tweets.append(
        "👀 What to Watch:\n\n"
        "• Nvidia Q3 earnings (AI bellwether)\n"
        "• Holiday retail performance (consumer strength test)\n"
        "• Private credit markets (bubble risk)\n"
        "• Fed signals on inflation persistence\n"
        "• AI capex vs revenue growth trends"
    )

    # Tweet 13: Key Takeaway
    tweets.append(
        "💡 Bottom Line:\n\n"
        "This isn't a market prediction - it's a complexity map. "
        "Every sector is transforming simultaneously. Smart strategy: "
        "Stay diversified, avoid FOMO, position-size carefully, watch the intersections not just individual stories."
    )

    # Tweet 14: Sources & Methodology
    tweets.append(
        "📚 Methodology:\n\n"
        "Analyzed 40 headlines from Business Insider (20) & Forbes (20)\n"
        "Grouped by themes, identified interconnections, mapped implications\n\n"
        "This thread synthesizes patterns across sources to reveal what really matters.\n\n"
        "#BusinessNews #Markets #AI"
    )

    return tweets

def post_thread(tweets):
    """Post a thread of tweets to Twitter"""

    try:
        # Authenticate
        client = tweepy.Client(
            bearer_token=BEARER_TOKEN,
            consumer_key=API_KEY,
            consumer_secret=API_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET,
            wait_on_rate_limit=True
        )

        tweet_count = len(tweets)
        print(f"Posting thread with {tweet_count} tweets...")

        # Post first tweet
        first_tweet_text = tweets[0]
        if len(first_tweet_text) > 280:
            print(f"⚠️  First tweet too long ({len(first_tweet_text)} chars), truncating...")
            first_tweet_text = first_tweet_text[:277] + "..."

        print(f"\n1/{tweet_count}: {first_tweet_text[:50]}...")
        response = client.create_tweet(text=first_tweet_text)
        previous_tweet_id = response.data['id']
        print(f"✅ Posted tweet 1 (ID: {previous_tweet_id})")
        time.sleep(1)  # Be nice to the API

        # Post remaining tweets as replies
        for i, tweet_text in enumerate(tweets[1:], start=2):
            # Check length
            if len(tweet_text) > 280:
                print(f"⚠️  Tweet {i} too long ({len(tweet_text)} chars), truncating...")
                tweet_text = tweet_text[:277] + "..."

            print(f"\n{i}/{tweet_count}: {tweet_text[:50]}...")
            response = client.create_tweet(
                text=tweet_text,
                in_reply_to_tweet_id=previous_tweet_id
            )
            previous_tweet_id = response.data['id']
            print(f"✅ Posted tweet {i} (ID: {previous_tweet_id})")
            time.sleep(1)  # Be nice to the API

        print(f"\n🎉 Successfully posted complete thread!")
        print(f"Thread ID: {previous_tweet_id}")
        return previous_tweet_id

    except tweepy.TweepyException as e:
        print(f"❌ Error posting to Twitter: {e}")
        raise

if __name__ == "__main__":
    print("Creating insightful business news thread...")
    tweets = create_insightful_thread()

    print(f"\nThread preview ({len(tweets)} tweets):")
    for i, tweet in enumerate(tweets, 1):
        print(f"\n--- Tweet {i}/{len(tweets)} ({len(tweet)} chars) ---")
        print(tweet)

    print("\n" + "="*60)
    print("Posting to Twitter...")
    print("="*60 + "\n")

    thread_id = post_thread(tweets)
    print(f"\n✅ Thread posted successfully! Final tweet ID: {thread_id}")
