---
name: linkedin-automation
description: |
  Automate LinkedIn posting to generate business leads and engagement. Creates and publishes
  posts about your business, services, and insights. Use when you need to maintain consistent
  LinkedIn presence for sales generation and brand awareness.
---

# LinkedIn Automation

Automate LinkedIn posting for business development and lead generation.

## Prerequisites

1. LinkedIn account with posting permissions
2. Playwright MCP server (for browser automation)
3. LinkedIn credentials stored securely

## Setup

### 1. Configure LinkedIn Credentials

Create `scripts/linkedin-config.json`:

```json
{
  "email": "your-email@example.com",
  "password": "use-environment-variable",
  "posting_schedule": {
    "frequency": "daily",
    "time": "09:00",
    "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
  },
  "content_themes": [
    "industry_insights",
    "company_updates",
    "case_studies",
    "tips_and_tricks"
  ]
}
```

### 2. Set Environment Variables

```bash
export LINKEDIN_EMAIL="your-email@example.com"
export LINKEDIN_PASSWORD="your-secure-password"
```

## Quick Reference

### Post to LinkedIn

```bash
# Using the skill
python3 scripts/linkedin-post.py --content "Your post content here"

# With image
python3 scripts/linkedin-post.py --content "Post with image" --image "path/to/image.png"

# Schedule post
python3 scripts/linkedin-post.py --content "Scheduled post" --schedule "2026-03-18 09:00"
```

### Generate Post Content

```bash
# AI-generated post based on business context
python3 scripts/generate-post.py --theme "industry_insights" --vault-path "../../Vault"
```

## Workflow: Automated Posting

1. **Content Generation**: AI analyzes business context from vault
2. **Draft Creation**: Generates LinkedIn post with hashtags
3. **Human Review**: Saves draft to `Vault/Pending_Approval/`
4. **Approval**: User reviews and approves
5. **Publishing**: Posts to LinkedIn via Playwright
6. **Tracking**: Logs post URL and timestamp

## Post Templates

### Industry Insight
```markdown
🚀 [Insight Title]

[2-3 paragraphs of valuable content]

Key takeaways:
• Point 1
• Point 2
• Point 3

What's your experience with this? Share in comments! 👇

#Industry #Business #Growth
```

### Company Update
```markdown
📢 Exciting news from [Company Name]!

[Update details]

This means [benefit to audience]

Learn more: [link]

#CompanyNews #Innovation
```

## Integration with Playwright

The skill uses the browsing-with-playwright skill for automation:

```bash
# Start Playwright server
bash ../browsing-with-playwright/scripts/start-server.sh

# Post to LinkedIn
python3 scripts/linkedin-post.py --content "Your content"

# Stop server
bash ../browsing-with-playwright/scripts/stop-server.sh
```

## Content Strategy

### Posting Frequency
- **Minimum**: 3 posts per week
- **Optimal**: 1 post per day (weekdays)
- **Maximum**: 2 posts per day

### Best Times to Post
- **Morning**: 7:00-9:00 AM (before work)
- **Lunch**: 12:00-1:00 PM (lunch break)
- **Evening**: 5:00-6:00 PM (after work)

### Content Mix (80/20 Rule)
- 80% Value: Tips, insights, education
- 20% Promotion: Services, offers, CTAs

## Automation Features

### Smart Content Generation
- Analyzes recent business activities from vault
- Generates relevant posts based on context
- Includes appropriate hashtags and CTAs

### Engagement Tracking
- Saves post URLs for later analysis
- Tracks posting schedule compliance
- Monitors approval workflow

### Safety Features
- All posts require human approval
- Preview before publishing
- Rollback capability for drafts

## Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| auto_hashtags | true | Automatically add relevant hashtags |
| max_hashtags | 5 | Maximum hashtags per post |
| require_approval | true | Require human approval before posting |
| save_drafts | true | Save drafts to Pending_Approval folder |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Login failed | Check credentials in environment variables |
| Post not appearing | LinkedIn may have rate limits, wait 1 hour |
| Image upload failed | Ensure image is < 5MB and PNG/JPG format |
| Playwright timeout | Increase timeout in config or check internet |

## Security Notes

- Never store passwords in config files
- Use environment variables or secure vault
- Enable 2FA on LinkedIn account
- Monitor for suspicious login attempts

## Verification

Run: `python3 scripts/verify-linkedin.py`

Expected: `✓ LinkedIn credentials valid, ready to post`
