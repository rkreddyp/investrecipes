#!/usr/bin/env python3
"""
Twitter Thread Poster - Market Analysis Thread
Posts insightful analysis of AI bubble concerns and market dynamics
"""

import tweepy
import time
from datetime import datetime

# Twitter API Credentials
API_KEY = "KiEaJHzFUWE7BLPMrMeABVx8z"
API_SECRET = "GSvXTcUGpA37xZ5pKOu2aMitplfM0icbrlnVnwbZNVIJVaNQbT"
ACCESS_TOKEN = "1088426905634779136-fKvck5gh92Z5nrirFvkYlfM3ftyZ43"
ACCESS_TOKEN_SECRET = "Rsf3g4rpADKm6U42QbIxjI82kAt2kUVbDFBrCS1ELTmU8"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAALL3wQEAAAAAEU16sJsJT9zl7D0w6iGMky%2FXn5I%3D3bCPWBSMOyKAlF7LfbRTCbIlt8goxzq2lZlEC6jfcdZNzPU7Jv"

def create_twitter_client():
    """Create and return authenticated Twitter API v2 client"""
    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
        wait_on_rate_limit=True
    )
    return client

def post_thread(client, tweets):
    """
    Post a thread of tweets

    Args:
        client: Tweepy Client instance
        tweets: List of tweet texts

    Returns:
        List of tweet IDs
    """
    tweet_ids = []
    previous_tweet_id = None

    for i, tweet_text in enumerate(tweets, 1):
        try:
            # Add thread numbering
            numbered_tweet = f"{tweet_text}\n\n{i}/{len(tweets)}"

            # Post tweet (reply to previous if in thread)
            if previous_tweet_id:
                response = client.create_tweet(
                    text=numbered_tweet,
                    in_reply_to_tweet_id=previous_tweet_id
                )
            else:
                response = client.create_tweet(text=numbered_tweet)

            tweet_id = response.data['id']
            tweet_ids.append(tweet_id)
            previous_tweet_id = tweet_id

            print(f"✅ Posted tweet {i}/{len(tweets)}: {tweet_id}")

            # Rate limit protection - wait between tweets
            if i < len(tweets):
                time.sleep(2)

        except tweepy.TweepyException as e:
            print(f"❌ Error posting tweet {i}: {e}")
            raise

    return tweet_ids

def main():
    """Main function to post market analysis thread"""

    # Thread content - Insightful, Educational, Intuitive
    thread = [
        # Tweet 1: Hook - Clear overview of what's happening
        "🧵 Markets are flashing warning signs as AI investment mania meets reality. Here's what's happening and why it matters for your portfolio:",

        # Tweet 2: Context - AI bubble debate intensifies
        "The AI bubble debate just got real. Forbes reports a TRILLION DOLLAR borrowing binge for AI infrastructure that could spark the next credit crunch.\n\nThis isn't just hype - it's about massive debt accumulation in an unproven sector.",

        # Tweet 3: Insight - Nvidia earnings as a bellwether
        "All eyes on Nvidia's Q3 earnings (Nov 19). Why does one company's earnings matter so much?\n\nBecause Nvidia = AI infrastructure. Their numbers reveal whether the AI spending boom is sustainable or overheated.",

        # Tweet 4: Insight - Market structure concerns
        "Here's the pattern: Markets stumbling on Fed signals + AI crosscurrents + earnings volatility (per Forbes).\n\nTranslation: Investors are losing confidence that AI investments will pay off before interest rates bite.",

        # Tweet 5: Educational - Explaining the mechanism
        "Why AI debt matters:\n\n1️⃣ Companies borrow heavily to build AI infrastructure\n2️⃣ High interest rates make that debt expensive\n3️⃣ If AI revenue doesn't materialize fast enough...\n4️⃣ Credit crunch = 2008-style cascade",

        # Tweet 6: Counterpoint - Bull case still exists
        "BUT: Jefferies flags 4 charts showing the sell-off could turn into a NEW RALLY.\n\nThe bull case? We're in an infrastructure build-out phase. Like railroads in 1800s or internet in 1990s, initial losses don't mean the tech is wrong.",

        # Tweet 7: Corporate governance wild card
        "Wild card: OpenAI board drama. Larry Summers just resigned over Epstein ties (both Forbes & BI confirm).\n\nWhy it matters: Governance chaos at AI's biggest names adds uncertainty when markets already doubt AI valuations.",

        # Tweet 8: Real economy impact
        "Real economy signal: Small businesses planning PRICE HIKES as inflation escalates (Forbes).\n\nThis pressures the Fed to keep rates high = more pressure on AI debt = tighter credit = potential bubble pop.",

        # Tweet 9: What to watch
        "What to watch:\n\n📊 Nvidia earnings (Nov 19) - beats expectations?\n🏦 Fed signals - dovish or hawkish?\n💰 AI startup funding - drying up?\n📉 Credit spreads - widening?\n\nThese will tell us if AI winter is coming or just FUD.",

        # Tweet 10: Synthesis and takeaway
        "Bottom line:\n\nAI is transformative tech. But trillion-dollar debt + high rates + unproven business models = dangerous cocktail.\n\nThe difference between 1999 (bubble) and 2009 (foundation) was timing, not technology.\n\nStay informed. Manage risk. 📈",

        # Tweet 11: Source attribution
        "Sources: Business Insider, Forbes market coverage (Nov 18-19, 2025)\n\nKey articles:\n• AI borrowing binge credit crunch warning\n• Nvidia Q3 earnings preview\n• Small business inflation pressure\n• Markets stumble on Fed signals\n• Jefferies rally charts"
    ]

    try:
        # Create Twitter client
        print("🔐 Authenticating with Twitter API...")
        client = create_twitter_client()

        # Verify credentials
        me = client.get_me()
        print(f"✅ Authenticated as: @{me.data.username}")

        # Post thread
        print(f"\n📤 Posting thread ({len(thread)} tweets)...\n")
        tweet_ids = post_thread(client, thread)

        # Summary
        print(f"\n✅ Thread posted successfully!")
        print(f"📊 Total tweets: {len(tweet_ids)}")
        print(f"🔗 Thread URL: https://twitter.com/{me.data.username}/status/{tweet_ids[0]}")

        # Save thread metadata
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"/Users/venkat/workfolder/playwright-min/outputs/twitter_poster/default/reports/thread_log_{timestamp}.txt"

        with open(log_file, 'w') as f:
            f.write(f"Market Analysis Thread Posted\n")
            f.write(f"{'='*50}\n\n")
            f.write(f"Posted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Username: @{me.data.username}\n")
            f.write(f"Thread URL: https://twitter.com/{me.data.username}/status/{tweet_ids[0]}\n")
            f.write(f"Total Tweets: {len(tweet_ids)}\n\n")
            f.write(f"Tweet IDs:\n")
            for i, tid in enumerate(tweet_ids, 1):
                f.write(f"  {i}. {tid}\n")
            f.write(f"\n{'='*50}\n\n")
            f.write("Thread Content:\n\n")
            for i, tweet in enumerate(thread, 1):
                f.write(f"Tweet {i}/{len(thread)}:\n{tweet}\n\n")

        print(f"📝 Thread log saved: {log_file}")

        return tweet_ids

    except tweepy.TweepyException as e:
        print(f"❌ Twitter API Error: {e}")
        raise
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        raise

if __name__ == "__main__":
    main()
