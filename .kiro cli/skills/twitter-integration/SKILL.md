# Twitter/X Integration Skill

## Overview
Monitors Twitter mentions and keywords, creates action files, and enables posting tweets.

## Features
- ✅ Monitor Twitter mentions
- ✅ Track specific keywords
- ✅ Intelligent categorization
- ✅ Priority detection
- ✅ Action file generation
- ✅ Post tweets
- ✅ Reply to tweets
- ✅ Like and retweet
- ✅ Delete tweets
- ✅ Account information
- ✅ Daily activity summaries

## Installation

### Prerequisites
```bash
pip install requests python-dotenv
```

### Configuration
Add to `.env`:
```
TWITTER_BEARER_TOKEN=your_bearer_token
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
```

## Getting Twitter API Credentials

1. Go to https://developer.twitter.com/
2. Create a new app or use existing one
3. Generate Bearer Token (for read operations)
4. Generate Access Token & Secret (for write operations)
5. Ensure app has Read and Write permissions

## Usage

### Run Watcher (Test Mode)
```bash
cd ".kiro cli/skills/twitter-integration/scripts"
python twitter-watcher.py --once
```

### Run Watcher (Continuous)
```bash
python twitter-watcher.py
```

### Post Tweet
```bash
python twitter-poster.py --tweet "Your tweet here"
```

### Reply to Tweet
```bash
python twitter-poster.py --reply TWEET_ID --message "Your reply"
```

### Like Tweet
```bash
python twitter-poster.py --like TWEET_ID
```

### Retweet
```bash
python twitter-poster.py --retweet TWEET_ID
```

### Delete Tweet
```bash
python twitter-poster.py --delete TWEET_ID
```

### Get Account Info
```bash
python twitter-poster.py --info
```

## Configuration File

Edit `twitter-config.json`:
```json
{
  "check_interval": 300,
  "monitor_mentions": true,
  "priority_keywords": ["urgent", "asap"],
  "categories": {
    "customer_inquiry": ["price", "cost"],
    "support": ["help", "issue"],
    "feedback": ["love", "terrible"],
    "lead": ["interested", "contact"]
  },
  "track_keywords": ["your_brand", "your_product"]
}
```

## Output Files

### Action Files
Location: `Vault/Needs_Action/`

Example: `TWITTER_MENTION_username_2026-03-19_12-30-00.md`

### Logs
Location: `Vault/Logs/`
- Daily logs: `twitter-watcher-YYYY-MM-DD.log`
- Summaries: `twitter-summary-YYYY-MM-DD.md`

## Integration with AI Employee

The Twitter integration works seamlessly with your AI Employee workflow:

1. **Automatic Monitoring**: Checks Twitter every 5 minutes
2. **Action Files**: Creates markdown files in Vault/Needs_Action/
3. **Categorization**: Automatically categorizes interactions
4. **Priority Detection**: Flags urgent mentions
5. **Keyword Tracking**: Monitor brand mentions and keywords
6. **Odoo Integration**: Action files can trigger CRM updates

## API Limitations

- Twitter API v2 Free tier: 1,500 tweets per month
- Rate limits: 15 requests per 15 minutes for most endpoints
- Tweet length: 280 characters
- Elevated access required for some features

## Troubleshooting

### Authentication Errors
- Verify all tokens are correct
- Check app permissions (Read + Write)
- Ensure tokens haven't expired

### Rate Limit Errors
- Reduce check_interval in config
- Use Essential or Elevated access tier
- Monitor API usage in Twitter Developer Portal

## Gold Tier Features

This skill contributes to Gold Tier requirements:
- ✅ Social media integration (Twitter/X)
- ✅ Cross-domain integration (Personal + Business)
- ✅ Automated monitoring and action generation
- ✅ Comprehensive logging

## Next Steps

1. Create Twitter Developer account
2. Generate API credentials
3. Configure `.env` file
4. Run test: `python twitter-watcher.py --once`
5. Add keywords to track in config
6. Integrate with Odoo for CRM updates
7. Set up automated scheduling

---

*Part of Gold Tier AI Employee Implementation*
*Built with Claude Code - March 2026*
