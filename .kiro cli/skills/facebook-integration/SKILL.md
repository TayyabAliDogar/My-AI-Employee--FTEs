# Facebook Integration Skill

## Overview
Monitors Facebook Page comments and messages, creates action files, and enables posting content to Facebook.

## Features
- ✅ Monitor Facebook Page comments
- ✅ Monitor Facebook Page messages (Messenger)
- ✅ Intelligent categorization (customer inquiry, support, feedback, leads)
- ✅ Priority detection
- ✅ Action file generation
- ✅ Post text and images to Facebook
- ✅ Reply to comments
- ✅ Send private messages
- ✅ Page insights and analytics
- ✅ Daily activity summaries

## Installation

### Prerequisites
```bash
pip install requests python-dotenv
```

### Configuration
Add to `.env`:
```
INSTAGRAM_ACCESS_TOKEN=your_access_token
FACEBOOK_PAGE_ID=your_page_id  # Optional, will auto-detect
```

## Usage

### Run Watcher (Test Mode)
```bash
cd ".kiro cli/skills/facebook-integration/scripts"
python facebook-watcher.py --once
```

### Run Watcher (Continuous)
```bash
python facebook-watcher.py
```

### Post to Facebook
```bash
python facebook-poster.py --post "Your message here"
```

### Post with Link
```bash
python facebook-poster.py --post "Check this out!" --link "https://example.com"
```

### Post with Image
```bash
python facebook-poster.py --post "New product!" --image "https://example.com/image.jpg"
```

### Reply to Comment
```bash
python facebook-poster.py --reply COMMENT_ID --message "Thank you for your comment!"
```

### Send Private Message
```bash
python facebook-poster.py --send USER_ID --message "Hello!"
```

### Get Page Insights
```bash
python facebook-poster.py --insights
```

### Get Page Info
```bash
python facebook-poster.py --info
```

## Configuration File

Edit `facebook-config.json`:
```json
{
  "check_interval": 300,
  "priority_keywords": ["urgent", "asap", "important"],
  "categories": {
    "customer_inquiry": ["price", "cost", "buy"],
    "support": ["help", "issue", "problem"],
    "feedback": ["love", "great", "terrible"],
    "lead": ["interested", "more info", "contact"]
  },
  "monitor_comments": true,
  "monitor_messages": true
}
```

## Output Files

### Action Files
Location: `Vault/Needs_Action/`

Example: `FACEBOOK_COMMENT_JohnDoe_2026-03-19_12-30-00.md`

### Logs
Location: `Vault/Logs/`
- Daily logs: `facebook-watcher-YYYY-MM-DD.log`
- Summaries: `facebook-summary-YYYY-MM-DD.md`

## Integration with AI Employee

The Facebook integration works seamlessly with your AI Employee workflow:

1. **Automatic Monitoring**: Checks Facebook every 5 minutes (configurable)
2. **Action Files**: Creates markdown files in Vault/Needs_Action/
3. **Categorization**: Automatically categorizes interactions
4. **Priority Detection**: Flags urgent messages
5. **Odoo Integration**: Action files can trigger CRM updates

## API Requirements

- Facebook Business account
- Facebook Page
- Access token with permissions:
  - `pages_show_list`
  - `pages_read_engagement`
  - `pages_manage_posts`
  - `pages_manage_engagement`
  - `pages_messaging`

## Troubleshooting

### Authentication Errors
- Verify access token is valid
- Check token permissions
- Ensure you have admin access to the Page

### No Comments/Messages Found
- Check if Page has recent activity
- Verify API permissions
- Check rate limits (200 calls per hour)

## Gold Tier Features

This skill contributes to Gold Tier requirements:
- ✅ Social media integration (Facebook)
- ✅ Cross-domain integration (Personal + Business)
- ✅ Automated monitoring and action generation
- ✅ Comprehensive logging

## Next Steps

1. Set up Facebook Business account
2. Create Facebook Page
3. Generate access token with required permissions
4. Configure `.env` file
5. Run test: `python facebook-watcher.py --once`
6. Integrate with Odoo for CRM updates
7. Set up automated scheduling

---

*Part of Gold Tier AI Employee Implementation*
*Built with Claude Code - March 2026*
