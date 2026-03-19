# CEO Briefing Generator

## Overview
Automated weekly business audit and CEO briefing system that aggregates data from Odoo, social media, and action files to provide comprehensive business intelligence.

## Features
- ✅ Financial performance summary (revenue, expenses, profit/loss)
- ✅ Operations metrics (pending/completed actions)
- ✅ High-priority item tracking
- ✅ Social media activity summary
- ✅ CRM pipeline overview
- ✅ Bottleneck identification
- ✅ Actionable recommendations
- ✅ Trend analysis
- ✅ Automated weekly generation

## Installation

### Prerequisites
```bash
pip install python-dotenv
```

### Dependencies
- Odoo MCP Server (for financial data)
- All watcher skills (Gmail, Instagram, Facebook, Twitter, LinkedIn)

## Usage

### Generate Briefing (7 days)
```bash
cd ".kiro cli/skills/ceo-briefing/scripts"
python ceo-briefing-generator.py
```

### Generate Briefing (Custom Period)
```bash
python ceo-briefing-generator.py --days 30
```

### Generate and Print
```bash
python ceo-briefing-generator.py --print
```

### Schedule Weekly Briefing (Windows)
```powershell
# Create scheduled task for Monday 8 AM
schtasks /create /tn "CEO Briefing" /tr "python ceo-briefing-generator.py" /sc weekly /d MON /st 08:00
```

### Schedule Weekly Briefing (Linux/Mac)
```bash
# Add to crontab (Monday 8 AM)
0 8 * * 1 cd /path/to/scripts && python3 ceo-briefing-generator.py
```

## Output

### Briefing Location
`Vault/CEO_Briefings/CEO_Briefing_YYYY-MM-DD.md`

### Briefing Sections

1. **Executive Summary**
   - Financial performance
   - Operations overview
   - High-priority count

2. **Detailed Metrics**
   - Pending actions by platform
   - High-priority items list
   - Financial details
   - Sales pipeline

3. **Bottlenecks & Recommendations**
   - Identified issues
   - Severity levels
   - Actionable recommendations

4. **Trends & Insights**
   - Performance analysis
   - Concern flags
   - Positive indicators

5. **Next Steps**
   - Immediate actions
   - Weekly priorities
   - Strategic initiatives

## Data Sources

### Odoo Integration
- Revenue from customer invoices
- Expenses from vendor bills
- Outstanding invoices
- Payment records
- CRM leads and opportunities

### Action Files
- Pending actions count by platform
- Completed actions count
- High-priority items
- Response time metrics

### Social Media
- Instagram activity
- Facebook engagement
- Twitter mentions
- LinkedIn interactions

## Bottleneck Detection

The system automatically identifies:

1. **Operations Bottlenecks**
   - High pending action count (>50)
   - Slow response times
   - Platform-specific backlogs

2. **Cash Flow Issues**
   - High outstanding invoices (>10)
   - Low payment collection rate
   - Overdue payments

3. **Profitability Concerns**
   - Low profit margins (<20%)
   - High expense ratios
   - Revenue decline

## Example Briefing

```markdown
# CEO BRIEFING
**Period:** 2026-03-12 to 2026-03-19 (7 days)

## 📊 EXECUTIVE SUMMARY

### Financial Performance
📈 **Revenue:** 15,000.00 USD
💰 **Expenses:** 8,500.00 USD
💵 **Profit:** 6,500.00 USD
📊 **Margin:** 43.3%

### Operations
✅ **Completed Actions:** 45
⏳ **Pending Actions:** 23
🔴 **High Priority:** 5

## ⚠️ BOTTLENECKS & RECOMMENDATIONS

🔴 **Cash Flow**
- Issue: 12 unpaid invoices
- Recommendation: Follow up on overdue payments

## ✅ ACTION ITEMS
1. Review and respond to 5 high-priority items
2. Follow up on 12 outstanding invoices
3. Process 23 pending actions
```

## Integration with AI Employee

The CEO Briefing Generator is the culmination of the Gold Tier AI Employee:

1. **Monday Morning Ritual**: Automated briefing every Monday
2. **Data Aggregation**: Combines all business intelligence sources
3. **Proactive Management**: Identifies issues before they escalate
4. **Actionable Insights**: Provides clear next steps
5. **Trend Tracking**: Historical comparison and analysis

## Customization

Edit the script to customize:
- Bottleneck thresholds
- Report sections
- Metrics tracked
- Recommendation logic
- Output format

## Gold Tier Requirement

This skill is CRITICAL for Gold Tier:
- ✅ Weekly Business Audit (required)
- ✅ CEO Briefing generation (required)
- ✅ Cross-domain integration
- ✅ Automated business intelligence
- ✅ Proactive management

## Advanced Features

### Email Delivery
Integrate with email-sender skill to automatically email briefing:

```python
# Add to ceo-briefing-generator.py
from email_sender import send_email

send_email(
    to="ceo@company.com",
    subject=f"CEO Briefing - {date}",
    body=briefing
)
```

### Slack Integration
Post briefing to Slack channel:

```python
import requests

webhook_url = os.getenv("SLACK_WEBHOOK_URL")
requests.post(webhook_url, json={"text": briefing})
```

### Historical Comparison
Track metrics over time:

```python
# Compare with previous week
previous_briefing = load_previous_briefing()
growth_rate = calculate_growth(current, previous)
```

## Troubleshooting

### No Financial Data
- Ensure Odoo MCP Server is configured
- Check Odoo connection
- Verify accounting module is installed

### Missing Action Files
- Ensure watchers are running
- Check Vault directory structure
- Verify file permissions

### Empty Briefing
- Run watchers to generate action files
- Create sample invoices in Odoo
- Check date range parameters

## Next Steps

1. Set up Odoo accounting
2. Run all watchers to generate data
3. Test briefing generation: `python ceo-briefing-generator.py --print`
4. Schedule weekly automation
5. Customize thresholds and metrics
6. Add email/Slack delivery

---

*Part of Gold Tier AI Employee Implementation*
*The "Monday Morning CEO Briefing" - Autonomous Business Intelligence*
*Built with Claude Code - March 2026*
