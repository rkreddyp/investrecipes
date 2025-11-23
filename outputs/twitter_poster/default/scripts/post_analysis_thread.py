#!/usr/bin/env python3
"""
Post comprehensive market analysis as Twitter thread
Uses Twitter API v2 for thread creation
"""

import tweepy
import time

# Twitter API v2 credentials
API_KEY = "KiEaJHzFUWE7BLPMrMeABVx8z"
API_SECRET = "GSvXTcUGpA37xZ5pKOu2aMitplfM0icbrlnVnwbZNVIJVaNQbT"
ACCESS_TOKEN = "1088426905634779136-fKvck5gh92Z5nrirFvkYlfM3ftyZ43"
ACCESS_TOKEN_SECRET = "Rsf3g4rpADKm6U42QbIxjI82kAt2kUVbDFBrCS1ELTmU8"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAALL3wQEAAAAAEU16sJsJT9zl7D0w6iGMky%2FXn5I%3D3bCPWBSMOyKAlF7LfbRTCbIlt8goxzq2lZlEC6jfcdZNzPU7Jv"

def create_twitter_client():
    """Initialize Twitter API v2 client"""
    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )
    return client

def create_thread_tweets():
    """Create insightful, educational thread about market analysis"""

    tweets = [
        # Tweet 1: Hook - What happened and why it matters (1/15)
        """🧵 MARKET ANALYSIS: Nov 21, 2025

Analyzed 221 headlines from 15+ sources (Bloomberg, Reuters, CNBC, WSJ, etc.)

Today was the "wildest trading day since April's tariff shock."

Here's what's really happening and why it matters 👇

(1/15)""",

        # Tweet 2: The Three Converging Crises (2/15)
        """Three major forces converged to create today's chaos:

1️⃣ AI bubble fears despite strong earnings
2️⃣ Bitcoin's worst month since 2022 crash
3️⃣ Fed sending contradictory rate signals

Each alone would rattle markets. Together? Chaos.

(2/15)""",

        # Tweet 3: AI Paradox (3/15)
        """📊 THE AI PARADOX

Nvidia crushed earnings. Revenue up, guidance strong.

But the stock sold off hard.

CEO Jensen Huang (leaked memo): "The market did not appreciate it."

This is classic "sell the news" - when even GOOD news can't stop selling.

(3/15)""",

        # Tweet 4: What AI selloff means (4/15)
        """Why does the Nvidia selloff matter?

It signals investors are questioning if massive AI spending (~$100B+ by tech giants) will ever generate adequate returns.

When markets sell strong earnings, they're saying: "Your growth doesn't justify your valuation."

(4/15)""",

        # Tweet 5: Retail vs Institutions (5/15)
        """⚠️ DANGER SIGNAL: Sentiment Divergence

Wall Street institutions: SELLING
Main Street retail: BUYING

This gap is historically a red flag.

When pros and amateurs disagree this sharply, the pros are usually right (unfortunately).

(5/15)""",

        # Tweet 6: Bitcoin Crash (6/15)
        """₿ BITCOIN CRISIS

• Fell below $82K today
• Worst month since 2022 collapse
• "Flash crash" territory

Forbes: "Two big institutions triggered the crash"

Crypto isn't just correcting - it's in full retreat as risk appetite vanishes.

(6/15)""",

        # Tweet 7: Fed Whiplash (7/15)
        """🏛️ FED POLICY WHIPLASH

MORNING: NY Fed's Williams calls for rate cut
→ Markets rally

AFTERNOON: Boston Fed's Collins says rates "appropriate for now"
→ Markets reverse

Investors don't know whether December brings a cut or pause.

(7/15)""",

        # Tweet 8: Economic bifurcation (8/15)
        """📈 ECONOMIC SPLIT

Services sectors: BOOMING (fastest growth in 4 months)
Manufacturing: STRUGGLING

This "two-speed economy" makes Fed's job nearly impossible.

Cut rates to help manufacturing? Risk inflaming already-hot services sector.

(8/15)""",

        # Tweet 9: Labor market softening (9/15)
        """👷 LABOR MARKET SOFTENING

• September: Only 119K jobs added
• Unemployment: 4.4% (rising)
• Below pace needed to keep up with population growth

Not collapsing, but clearly cooling. Another headache for the Fed.

(9/15)""",

        # Tweet 10: The hidden problem (10/15)
        """💰 THE HIDDEN PROBLEM

Massive AI infrastructure spending may be masking economic weakness.

When Big Tech floods bond markets with AI capex, it inflates economic indicators.

But if AI doesn't deliver returns? That "growth" was artificial.

(10/15)""",

        # Tweet 11: Dip buying tested (11/15)
        """📉 DIP-BUYING STRATEGY UNDER FIRE

The "buy the dip" approach that's worked for years?

Facing its toughest test.

Even bullish strategist Tom Lee is adjusting positions.

When dip-buyers hesitate, volatility accelerates.

(11/15)""",

        # Tweet 12: The big contradiction (12/15)
        """❓ THE BIG CONTRADICTION

Equity funds: 5th straight week of INFLOWS
Global funds: 9th consecutive week of INFLOWS
Tech: On track for record $75B inflows (BofA)

Yet prices are FALLING hard.

Either flows are lagging OR retail is buying while institutions exit.

(12/15)""",

        # Tweet 13: What this means (13/15)
        """💡 WHAT THIS MEANS

The convergence of AI valuation questions, crypto instability, and Fed uncertainty has created a critical inflection point.

Market psychology is shifting from "buy dips" to "sell rallies."

That's a regime change.

(13/15)""",

        # Tweet 14: Key uncertainties (14/15)
        """🔮 KEY UNCERTAINTIES AHEAD

1. Will December bring Fed rate cut or pause?
2. Can AI spending justify current valuations?
3. Is crypto crash over or just beginning?
4. Why are fund flows positive while prices fall?

No clear answers yet.

(14/15)""",

        # Tweet 15: Takeaway (15/15)
        """🎯 BOTTOM LINE

Today wasn't just volatility - it was a test of core market assumptions.

Watch for:
✓ Fed clarity (or continued confusion)
✓ Whether dip-buying returns
✓ Retail-institutional sentiment gap

The market is demanding respect again.

(15/15) END"""
    ]

    return tweets

def post_thread(client, tweets):
    """Post a threaded series of tweets"""

    print("=" * 60)
    print("POSTING MARKET ANALYSIS THREAD TO TWITTER")
    print("=" * 60)

    previous_tweet_id = None
    posted_tweets = []

    for i, tweet_text in enumerate(tweets, 1):
        try:
            print(f"\nPosting tweet {i}/{len(tweets)}...")
            print(f"Preview: {tweet_text[:80]}...")

            # Post tweet (either as reply to previous or as new tweet)
            if previous_tweet_id:
                response = client.create_tweet(
                    text=tweet_text,
                    in_reply_to_tweet_id=previous_tweet_id
                )
            else:
                response = client.create_tweet(text=tweet_text)

            tweet_id = response.data['id']
            previous_tweet_id = tweet_id
            posted_tweets.append(tweet_id)

            print(f"✅ Tweet {i} posted (ID: {tweet_id})")

            # Rate limiting - wait 1 second between tweets
            if i < len(tweets):
                time.sleep(1)

        except tweepy.TweepyException as e:
            print(f"❌ Error posting tweet {i}: {e}")
            if "429" in str(e):
                print("Rate limit hit. Waiting 60 seconds...")
                time.sleep(60)
            else:
                raise

    return posted_tweets

def main():
    """Main execution"""

    # Initialize Twitter client
    print("Initializing Twitter API client...")
    client = create_twitter_client()
    print("✅ Client initialized")

    # Create thread content
    print("\nCreating thread content...")
    tweets = create_thread_tweets()
    print(f"✅ Created {len(tweets)} tweets for thread")

    # Post thread
    posted_ids = post_thread(client, tweets)

    # Summary
    print("\n" + "=" * 60)
    print("✅ THREAD POSTED SUCCESSFULLY!")
    print("=" * 60)
    print(f"📊 Total tweets: {len(posted_ids)}")
    print(f"🔗 Thread URL: https://twitter.com/user/status/{posted_ids[0]}")
    print(f"📝 Analysis: 221 headlines from 15+ sources")
    print(f"💡 Key insights: AI bubble, crypto crash, Fed whiplash")
    print("=" * 60)

if __name__ == "__main__":
    main()
