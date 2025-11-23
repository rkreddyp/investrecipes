#!/usr/bin/env python3
"""Post business news to Slack channel"""

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

# Format message for Slack
def format_news_message():
    message_blocks = []

    # Header
    message_blocks.append({
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": f"📰 Business News Digest - {datetime.now().strftime('%B %d, %Y')}"
        }
    })

    message_blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"*Total Headlines:* 40 from Business Insider & Forbes"
        }
    })

    message_blocks.append({"type": "divider"})

    # Business Insider section
    if news_data.get('business_insider'):
        message_blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*📊 Business Insider Top Stories*"
            }
        })

        # Top 5 headlines
        for i, article in enumerate(news_data['business_insider'][:5], 1):
            message_blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{i}. <{article['url']}|{article['headline']}>"
                }
            })

    message_blocks.append({"type": "divider"})

    # Forbes section
    if news_data.get('forbes'):
        message_blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*💼 Forbes Top Stories*"
            }
        })

        # Top 5 headlines
        for i, article in enumerate(news_data['forbes'][:5], 1):
            message_blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{i}. <{article['url']}|{article['headline']}>"
                }
            })

    message_blocks.append({"type": "divider"})

    # Footer with link to full report
    message_blocks.append({
        "type": "context",
        "elements": [{
            "type": "mrkdwn",
            "text": "💾 Full report with 40 headlines available in outputs/business_news_scraper/default/reports/business_news_report.md"
        }]
    })

    return message_blocks

# Post to Slack
def post_to_slack():
    blocks = format_news_message()

    headers = {
        "Authorization": f"Bearer {SLACK_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "channel": CHANNEL,
        "blocks": blocks,
        "text": f"Business News Digest - {datetime.now().strftime('%B %d, %Y')}"  # Fallback text
    }

    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers=headers,
        json=payload
    )

    result = response.json()

    if result.get("ok"):
        print(f"✅ Successfully posted to #{CHANNEL}")
        print(f"Message timestamp: {result.get('ts')}")
    else:
        print(f"❌ Error posting to Slack: {result.get('error')}")
        print(f"Full response: {json.dumps(result, indent=2)}")

    return result

if __name__ == "__main__":
    result = post_to_slack()
