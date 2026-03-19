import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent / "odoo-mcp-server" / "scripts"))

try:
    from odoo_mcp_server import OdooMCPServer
except ImportError:
    print("⚠️  Warning: Odoo MCP Server not found. Financial data will be unavailable.")
    OdooMCPServer = None

# Windows console encoding fix
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

# Paths
SCRIPT_DIR = Path(__file__).parent
VAULT_DIR = Path(__file__).parent.parent.parent.parent / "Vault"
NEEDS_ACTION_DIR = VAULT_DIR / "Needs_Action"
DONE_DIR = VAULT_DIR / "Done"
LOGS_DIR = VAULT_DIR / "Logs"
BRIEFINGS_DIR = VAULT_DIR / "CEO_Briefings"

# Create directories
BRIEFINGS_DIR.mkdir(parents=True, exist_ok=True)

def log_message(message):
    """Log message to console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def count_action_files_by_type():
    """Count action files by platform"""
    if not NEEDS_ACTION_DIR.exists():
        return {}

    counts = {
        'EMAIL': 0,
        'INSTAGRAM': 0,
        'FACEBOOK': 0,
        'TWITTER': 0,
        'LINKEDIN': 0,
        'WHATSAPP': 0,
        'OTHER': 0
    }

    for file in NEEDS_ACTION_DIR.glob("*.md"):
        filename = file.name.upper()
        found = False
        for platform in counts.keys():
            if filename.startswith(platform):
                counts[platform] += 1
                found = True
                break
        if not found:
            counts['OTHER'] += 1

    return counts

def count_completed_actions():
    """Count completed action files"""
    if not DONE_DIR.exists():
        return 0
    return len(list(DONE_DIR.glob("*.md")))

def get_high_priority_actions():
    """Get list of high priority pending actions"""
    if not NEEDS_ACTION_DIR.exists():
        return []

    high_priority = []

    for file in NEEDS_ACTION_DIR.glob("*.md"):
        try:
            content = file.read_text(encoding='utf-8')
            if 'Priority:** HIGH' in content or 'Priority: HIGH' in content:
                # Extract subject from first line
                lines = content.split('\n')
                subject = lines[0].replace('#', '').strip() if lines else file.name
                high_priority.append({
                    'file': file.name,
                    'subject': subject
                })
        except Exception as e:
            log_message(f"Error reading {file.name}: {e}")

    return high_priority

def get_social_media_summary(days=7):
    """Get social media activity summary"""
    date_from = datetime.now() - timedelta(days=days)

    summary = {
        'instagram': {'posts': 0, 'comments': 0, 'messages': 0},
        'facebook': {'posts': 0, 'comments': 0, 'messages': 0},
        'twitter': {'tweets': 0, 'mentions': 0, 'keywords': 0}
    }

    # Count from log files
    if LOGS_DIR.exists():
        for log_file in LOGS_DIR.glob("*-summary-*.md"):
            try:
                if log_file.stat().st_mtime < date_from.timestamp():
                    continue

                content = log_file.read_text(encoding='utf-8')

                if 'instagram' in log_file.name.lower():
                    # Parse Instagram summary
                    pass
                elif 'facebook' in log_file.name.lower():
                    # Parse Facebook summary
                    pass
                elif 'twitter' in log_file.name.lower():
                    # Parse Twitter summary
                    pass

            except Exception as e:
                log_message(f"Error reading {log_file.name}: {e}")

    return summary

def get_financial_summary(odoo_server, days=7):
    """Get financial summary from Odoo"""
    if not odoo_server:
        return None

    try:
        date_from = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        date_to = datetime.now().strftime('%Y-%m-%d')

        pl = odoo_server.get_profit_loss(date_from, date_to)
        outstanding = odoo_server.get_outstanding_invoices()
        payments = odoo_server.get_payments(date_from, date_to)

        return {
            'revenue': pl['revenue'],
            'expenses': pl['expenses'],
            'profit': pl['profit'],
            'margin': pl['margin'],
            'currency': pl['currency'],
            'outstanding_count': len(outstanding),
            'outstanding_total': sum(inv['amount_residual'] for inv in outstanding),
            'payments_count': len(payments),
            'payments_total': sum(p['amount'] for p in payments if p['payment_type'] == 'inbound')
        }

    except Exception as e:
        log_message(f"Error fetching financial data: {e}")
        return None

def get_crm_summary(odoo_server):
    """Get CRM summary from Odoo"""
    if not odoo_server:
        return None

    try:
        leads = odoo_server.get_leads(limit=100)

        return {
            'total_leads': len(leads),
            'expected_revenue': sum(lead.get('expected_revenue', 0) for lead in leads),
            'top_leads': leads[:5] if leads else []
        }

    except Exception as e:
        log_message(f"Error fetching CRM data: {e}")
        return None

def identify_bottlenecks(pending_actions, financial_data):
    """Identify business bottlenecks"""
    bottlenecks = []

    # Check pending actions
    if pending_actions['total'] > 50:
        bottlenecks.append({
            'type': 'Operations',
            'issue': f'{pending_actions["total"]} pending actions',
            'severity': 'HIGH',
            'recommendation': 'Consider hiring additional support or automating responses'
        })

    # Check outstanding invoices
    if financial_data and financial_data['outstanding_count'] > 10:
        bottlenecks.append({
            'type': 'Cash Flow',
            'issue': f'{financial_data["outstanding_count"]} unpaid invoices',
            'severity': 'HIGH',
            'recommendation': 'Follow up on overdue payments, consider payment reminders'
        })

    # Check profit margin
    if financial_data and financial_data['margin'] < 20:
        bottlenecks.append({
            'type': 'Profitability',
            'issue': f'Low profit margin ({financial_data["margin"]:.1f}%)',
            'severity': 'MEDIUM',
            'recommendation': 'Review pricing strategy and reduce operational costs'
        })

    return bottlenecks

def generate_ceo_briefing(days=7):
    """Generate comprehensive CEO briefing"""
    log_message("=" * 60)
    log_message("GENERATING CEO BRIEFING")
    log_message("=" * 60)

    # Initialize Odoo connection
    odoo_server = None
    if OdooMCPServer:
        try:
            odoo_server = OdooMCPServer()
            if odoo_server.connect():
                log_message("✓ Connected to Odoo")
            else:
                odoo_server = None
                log_message("⚠️  Odoo connection failed - financial data unavailable")
        except Exception as e:
            log_message(f"⚠️  Odoo error: {e}")
            odoo_server = None

    # Gather data
    log_message("Gathering business intelligence...")

    action_counts = count_action_files_by_type()
    completed_count = count_completed_actions()
    high_priority = get_high_priority_actions()
    social_summary = get_social_media_summary(days)
    financial_data = get_financial_summary(odoo_server, days)
    crm_data = get_crm_summary(odoo_server)

    pending_total = sum(action_counts.values())
    bottlenecks = identify_bottlenecks({'total': pending_total}, financial_data)

    # Generate briefing
    date_from = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    date_to = datetime.now().strftime('%Y-%m-%d')

    briefing = f"""# CEO BRIEFING
**Period:** {date_from} to {date_to} ({days} days)
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📊 EXECUTIVE SUMMARY

"""

    # Financial Summary
    if financial_data:
        profit_emoji = "📈" if financial_data['profit'] > 0 else "📉"
        briefing += f"""### Financial Performance

{profit_emoji} **Revenue:** {financial_data['revenue']:,.2f} {financial_data['currency']}
💰 **Expenses:** {financial_data['expenses']:,.2f} {financial_data['currency']}
💵 **Profit:** {financial_data['profit']:,.2f} {financial_data['currency']}
📊 **Margin:** {financial_data['margin']:.1f}%

"""
    else:
        briefing += """### Financial Performance

⚠️  *Financial data unavailable - Odoo connection required*

"""

    # Operations Summary
    briefing += f"""### Operations

✅ **Completed Actions:** {completed_count}
⏳ **Pending Actions:** {pending_total}
🔴 **High Priority:** {len(high_priority)}

"""

    # Detailed Breakdown
    briefing += f"""---

## 📈 DETAILED METRICS

### Pending Actions by Platform

"""

    for platform, count in sorted(action_counts.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            briefing += f"- **{platform}:** {count}\n"

    # High Priority Items
    if high_priority:
        briefing += f"""
### 🔴 High Priority Items ({len(high_priority)})

"""
        for item in high_priority[:10]:  # Show top 10
            briefing += f"- {item['subject']}\n"

    # Financial Details
    if financial_data:
        briefing += f"""
### 💰 Financial Details

**Cash Flow:**
- Payments Received: {financial_data['payments_count']} ({financial_data['payments_total']:,.2f} {financial_data['currency']})
- Outstanding Invoices: {financial_data['outstanding_count']} ({financial_data['outstanding_total']:,.2f} {financial_data['currency']})

"""

    # CRM Summary
    if crm_data:
        briefing += f"""### 🎯 Sales Pipeline

- Active Leads: {crm_data['total_leads']}
- Expected Revenue: {crm_data['expected_revenue']:,.2f}

"""

    # Bottlenecks
    if bottlenecks:
        briefing += f"""---

## ⚠️  BOTTLENECKS & RECOMMENDATIONS

"""
        for bottleneck in bottlenecks:
            severity_emoji = "🔴" if bottleneck['severity'] == 'HIGH' else "🟡"
            briefing += f"""
{severity_emoji} **{bottleneck['type']}**
- Issue: {bottleneck['issue']}
- Recommendation: {bottleneck['recommendation']}

"""

    # Action Items
    briefing += f"""---

## ✅ ACTION ITEMS

1. Review and respond to {len(high_priority)} high-priority items
2. Follow up on {financial_data['outstanding_count'] if financial_data else 'N/A'} outstanding invoices
3. Process {pending_total} pending actions across all platforms
4. Review and optimize operations based on bottlenecks identified

---

## 📊 TRENDS & INSIGHTS

"""

    # Add insights based on data
    if financial_data:
        if financial_data['profit'] > 0:
            briefing += f"✅ **Positive:** Business is profitable with {financial_data['margin']:.1f}% margin\n"
        else:
            briefing += f"⚠️  **Concern:** Business is operating at a loss\n"

    if pending_total > 20:
        briefing += f"⚠️  **Concern:** High volume of pending actions may indicate capacity issues\n"

    if financial_data and financial_data['outstanding_total'] > financial_data['revenue'] * 0.3:
        briefing += f"⚠️  **Concern:** Outstanding invoices represent significant portion of revenue\n"

    briefing += f"""
---

## 🎯 NEXT STEPS

1. **Immediate (Today):**
   - Address all high-priority items
   - Review cash flow and outstanding payments

2. **This Week:**
   - Clear pending action backlog
   - Follow up on leads in CRM
   - Optimize bottleneck areas

3. **Strategic:**
   - Review pricing and margins
   - Evaluate automation opportunities
   - Plan for capacity scaling

---

*Generated by AI Employee - CEO Briefing Generator*
*Powered by Claude Code & Odoo Integration*
*{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

    # Save briefing
    filename = f"CEO_Briefing_{datetime.now().strftime('%Y-%m-%d')}.md"
    filepath = BRIEFINGS_DIR / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(briefing)

    log_message(f"✅ CEO Briefing saved: {filename}")
    log_message("=" * 60)

    return filepath, briefing

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="CEO Briefing Generator")
    parser.add_argument('--days', type=int, default=7, help='Number of days to include in report (default: 7)')
    parser.add_argument('--print', action='store_true', help='Print briefing to console')

    args = parser.parse_args()

    filepath, briefing = generate_ceo_briefing(days=args.days)

    if args.print:
        print("\n" + "=" * 60)
        print(briefing)
        print("=" * 60)

    print(f"\n📄 Briefing saved to: {filepath}")
