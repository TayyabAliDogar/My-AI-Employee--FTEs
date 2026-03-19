# Instagram Watcher & Poster Skill

## Overview
Monitors Instagram messages and comments, creates action files, and enables posting content to Instagram.

## Features
- ✅ Monitor Instagram direct messages
- ✅ Monitor comments on posts
- ✅ Intelligent categorization (customer inquiry, support, feedback, collaboration)
- ✅ Priority detection
- ✅ Action file generation
- ✅ Post images to Instagram feed
- ✅ Post Instagram stories
- ✅ Reply to comments
- ✅ Account insights and analytics
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
INSTAGRAM_ACCOUNT_ID=your_account_id
```

## Usage

### Run Watcher (Test Mode)
```bash
cd ".kiro cli/skills/instagram-watcher/scripts"
python instagram-watcher.py --once
```

### Run Watcher (Continuous)
```bash
python instagram-watcher.py
```

### Post to Instagram
```bash
python instagram-poster.py --post "https://example.com/image.jpg" --caption "Your caption here"
```

### Post Story
```bash
python instagram-poster.py --story "https://example.com/image.jpg"
```

### Reply to Comment
```bash
python instagram-poster.py --reply COMMENT_ID --message "Thank you for your comment!"
```

### Get Account Insights
```bash
python instagram-poster.py --insights
```

## Configuration File

Edit `instagram-config.json`:
```json
{
  "check_interval": 300,
  "priority_keywords": ["urgent", "asap", "important"],
  "categories": {
    "customer_inquiry": ["price", "cost", "buy"],
    "support": ["help", "issue", "problem"],
    "feedback": ["love", "great", "terrible"],
    "collaboration": ["collab", "partnership"]
  }
}
```

## Output Files

### Action Files
Location: `Vault/Needs_Action/`

Example: `INSTAGRAM_MESSAGE_username_2026-03-19_12-30-00.md`

### Logs
Location: `Vault/Logs/`
- Daily logs: `instagram-watcher-YYYY-MM-DD.log`
- Summaries: `instagram-summary-YYYY-MM-DD.md`

## Integration with AI Employee

The Instagram watcher integrates seamlessly with your AI Employee workflow:

1. **Automatic Monitoring**: Checks Instagram every 5 minutes (configurable)
2. **Action Files**: Creates markdown files in Vault/Needs_Action/
3. **Categorization**: Automatically categorizes interactions
4. **Priority Detection**: Flags urgent messages
5. **Odoo Integration**: Action files can trigger CRM updates

## API Limitations

- Instagram Graph API requires a Facebook Business account
- Access tokens expire and need renewal
- Rate limits apply (200 calls per hour per user)
- Some features require specific permissions

## Troubleshooting

### Authentication Errors
- Verify access token is valid
- Check token permissions include `instagram_basic`, `instagram_manage_messages`, `instagram_manage_comments`
- Ensure account is a Business or Creator account

### No Messages/Comments Found
- Check if account has unread messages
- Verify API permissions
- Check rate limits

## Gold Tier Features

This skill contributes to Gold Tier requirements:
- ✅ Social media integration (Instagram)
- ✅ Cross-domain integration (Personal + Business)
- ✅ Automated monitoring and action generation
- ✅ Comprehensive logging

## Next Steps

1. Set up Facebook Business account
2. Generate Instagram access token
3. Configure `.env` file
4. Run test: `python instagram-watcher.py --once`
5. Integrate with Odoo for CRM updates
6. Set up automated scheduling

---

*Part of Gold Tier AI Employee Implementation*
*Built with Claude Code - March 2026*
