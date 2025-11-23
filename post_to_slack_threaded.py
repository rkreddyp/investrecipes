#!/usr/bin/env python3
"""Post business news to Slack channel with topic analysis and threading"""

import json
import requests
from datetime import datetime
from collections import defaultdict

# Slack configuration
import os
SLACK_TOKEN = os.getenv("SLACK_TOKEN", "your-slack-token-here")
CHANNEL = os.getenv("SLACK_CHANNEL", "stock_ops_dev")

# Load the news data
with open('/Users/venkat/workfolder/playwright-min/outputs/business_news_scraper/default/raw/headlines.json', 'r') as f:
    news_data = json.load(f)

def analyze_topics(headlines):
    """Analyze headlines and group by topics"""
    topics = defaultdict(list)

    # Combine all headlines
    all_articles = []
    for article in news_data.get('business_insider', []):
        all_articles.append({'headline': article['headline'], 'url': article['url'], 'source': 'Business Insider'})
    for article in news_data.get('forbes', []):
        all_articles.append({'headline': article['headline'], 'url': article['url'], 'source': 'Forbes'})

    # Topic keywords and classification
    topic_keywords = {
        'AI & Technology': ['ai', 'nvidia', 'openai', 'artificial intelligence', 'tech', 'microsoft', 'tesla', 'robot', 'cybercab', 'seo', 'geo'],
        'Corporate Leadership & Governance': ['ceo', 'exec', 'board', 'resign', 'summers', 'leadership', 'founder'],
        'Markets & Economy': ['market', 'stock', 'earning', 'rally', 'sell-off', 'fed', 'inflation', 'volatility', 'ipo', 'billionaire'],
        'Retail & Consumer': ['target', 'walmart', 'consumer', 'retail', 'shopping', 'thanksgiving'],
        'Business & Finance': ['trump', 'saudi', 'business', 'small business', 'price hike', 'mortgage', 'wealthfront'],
        'Healthcare & Biotech': ['eli lilly', 'healthcare', 'cancer', 'biotech', 'drug', 'caregiving'],
        'Workplace & Careers': ['job', 'hire', 'career', 'skills', 'navy', 'shipbuilder', 'soft skills'],
    }

    # Classify articles by topic
    for article in all_articles:
        headline_lower = article['headline'].lower()
        matched = False

        for topic, keywords in topic_keywords.items():
            if any(keyword in headline_lower for keyword in keywords):
                topics[topic].append(article)
                matched = True
                break

        if not matched:
            topics['Other News'].append(article)

    # Remove empty topics and sort by article count
    topics = {k: v for k, v in topics.items() if v}
    topics = dict(sorted(topics.items(), key=lambda x: len(x[1]), reverse=True))

    return topics, all_articles

def create_main_message(topics, total_count):
    """Create the main summary message"""
    blocks = []

    # Header
    blocks.append({
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": f"📰 Business News Digest - {datetime.now().strftime('%B %d, %Y')}"
        }
    })

    # Big picture summary
    summary_text = f"*{total_count} stories analyzed across {len(topics)} major topics*\n\n"
    summary_text += "*🔍 Today's Big Picture:*\n"

    # Add topic summary
    for i, (topic, articles) in enumerate(topics.items(), 1):
        count = len(articles)
        article_word = "story" if count == 1 else "stories"
        summary_text += f"• *{topic}*: {count} {article_word}\n"

    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": summary_text
        }
    })

    blocks.append({"type": "divider"})

    # Key insights
    insights = []

    for topic, articles in list(topics.items())[:3]:  # Top 3 topics
        if 'AI' in topic:
            insights.append(f"🤖 *AI dominates headlines* with {len(articles)} stories covering Nvidia earnings, OpenAI board changes, and the AI bubble debate")
        elif 'Market' in topic or 'Economy' in topic:
            insights.append(f"📈 *Market volatility* featured in {len(articles)} stories about earnings, Fed signals, and stock movements")
        elif 'Leadership' in topic or 'Corporate' in topic:
            insights.append(f"👔 *Corporate governance* in focus with {len(articles)} stories on executive changes and board resignations")
        elif 'Retail' in topic:
            insights.append(f"🛒 *Retail sector struggles* highlighted in {len(articles)} stories about Target, Walmart, and holiday shopping")

    if insights:
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "\n".join(insights)
            }
        })
        blocks.append({"type": "divider"})

    # Footer
    blocks.append({
        "type": "context",
        "elements": [{
            "type": "mrkdwn",
            "text": "🧵 _Detailed stories by topic in thread below_ | 💾 Full report: outputs/business_news_scraper/default/reports/"
        }]
    })

    return blocks

def create_topic_thread_message(topic, articles):
    """Create a threaded message for a specific topic"""
    blocks = []

    # Topic header
    emoji_map = {
        'AI & Technology': '🤖',
        'Markets & Economy': '📈',
        'Corporate Leadership & Governance': '👔',
        'Retail & Consumer': '🛒',
        'Business & Finance': '💼',
        'Healthcare & Biotech': '🏥',
        'Workplace & Careers': '💼',
        'Other News': '📰'
    }

    emoji = emoji_map.get(topic, '📌')
    count = len(articles)
    article_word = "Story" if count == 1 else "Stories"

    blocks.append({
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": f"{emoji} {topic} ({count} {article_word})"
        }
    })

    # List articles
    for i, article in enumerate(articles, 1):
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"{i}. <{article['url']}|{article['headline']}>\n_Source: {article['source']}_"
            }
        })

        # Add divider between articles (except last one)
        if i < len(articles):
            blocks.append({"type": "divider"})

    return blocks

def post_to_slack():
    """Post main message and topic threads to Slack"""
    topics, all_articles = analyze_topics(news_data)

    headers = {
        "Authorization": f"Bearer {SLACK_TOKEN}",
        "Content-Type": "application/json"
    }

    # Post main message
    main_blocks = create_main_message(topics, len(all_articles))
    main_payload = {
        "channel": CHANNEL,
        "blocks": main_blocks,
        "text": f"Business News Digest - {datetime.now().strftime('%B %d, %Y')}"
    }

    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers=headers,
        json=main_payload
    )

    main_result = response.json()

    if not main_result.get("ok"):
        print(f"❌ Error posting main message: {main_result.get('error')}")
        return main_result

    print(f"✅ Posted main message to #{CHANNEL}")
    thread_ts = main_result.get("ts")

    # Post topic threads
    for topic, articles in topics.items():
        topic_blocks = create_topic_thread_message(topic, articles)

        thread_payload = {
            "channel": CHANNEL,
            "thread_ts": thread_ts,  # Reply in thread
            "blocks": topic_blocks,
            "text": f"{topic} - {len(articles)} stories"
        }

        response = requests.post(
            "https://slack.com/api/chat.postMessage",
            headers=headers,
            json=thread_payload
        )

        result = response.json()
        if result.get("ok"):
            print(f"  ✅ Posted {topic} thread ({len(articles)} stories)")
        else:
            print(f"  ❌ Error posting {topic}: {result.get('error')}")

    print(f"\n🎉 Successfully posted digest with {len(topics)} topic threads")
    return main_result

if __name__ == "__main__":
    result = post_to_slack()
