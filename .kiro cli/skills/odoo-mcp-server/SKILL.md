# Odoo MCP Server

## Overview
Model Context Protocol (MCP) server for Odoo accounting and CRM integration. Provides comprehensive business intelligence and automation capabilities.

## Features
- ✅ Financial reporting (revenue, expenses, profit/loss)
- ✅ Invoice management
- ✅ Payment tracking
- ✅ Customer management
- ✅ CRM lead management
- ✅ Product catalog access
- ✅ Outstanding invoices tracking
- ✅ Business report generation
- ✅ Automated data synchronization

## Installation

### Prerequisites
```bash
pip install python-dotenv
```

### Odoo Setup
1. Install Odoo 19+ (Docker recommended)
2. Create database
3. Install accounting module
4. Configure user with API access

### Configuration
Add to `.env`:
```
ODOO_URL=https://your-odoo-instance.com
ODOO_DB=your_database
ODOO_USER=admin
ODOO_PASSWORD=your_password
```

## Usage

### Test Connection
```bash
cd ".kiro cli/skills/odoo-mcp-server/scripts"
python odoo-mcp-server.py
```

### Python Integration
```python
from odoo_mcp_server import OdooMCPServer

server = OdooMCPServer()
server.connect()

# Get revenue
revenue = server.get_revenue(date_from='2026-01-01')
print(f"Total Revenue: {revenue['total']}")

# Get profit/loss
pl = server.get_profit_loss(date_from='2026-01-01')
print(f"Profit: {pl['profit']}")

# Create lead
lead_id = server.create_lead(
    name="New Customer",
    email="customer@example.com",
    phone="+1234567890"
)
```

## API Methods

### Financial Methods

#### `get_invoices(state, date_from, date_to, limit)`
Get invoices with filters
- **state**: 'draft', 'posted', 'cancel'
- **date_from/to**: Date range (YYYY-MM-DD)
- **limit**: Max records (default 100)

#### `get_revenue(date_from, date_to)`
Calculate total revenue from customer invoices

#### `get_expenses(date_from, date_to)`
Calculate total expenses from vendor bills

#### `get_profit_loss(date_from, date_to)`
Calculate profit/loss with margin

#### `get_payments(date_from, date_to, limit)`
Get payment records

#### `get_outstanding_invoices()`
Get unpaid invoices

#### `create_invoice(partner_id, invoice_lines, invoice_type)`
Create new invoice

### CRM Methods

#### `get_leads(stage, limit)`
Get CRM leads/opportunities

#### `create_lead(name, email, phone, description)`
Create new lead

### Product Methods

#### `get_products(limit)`
Get product catalog

### Reporting Methods

#### `generate_business_report(days)`
Generate comprehensive business report
- Financial summary
- Outstanding invoices
- Recent payments
- Active leads

## Integration with AI Employee

The Odoo MCP Server enables:

1. **Automated Accounting**: Track revenue and expenses automatically
2. **CEO Briefings**: Generate weekly business reports
3. **Lead Management**: Auto-create leads from social media interactions
4. **Invoice Tracking**: Monitor outstanding payments
5. **Financial Alerts**: Notify on low cash flow or overdue invoices

## Example: Social Media to CRM

```python
# When Instagram message is received
server = OdooMCPServer()
server.connect()

# Create lead from Instagram inquiry
lead_id = server.create_lead(
    name=f"Instagram Lead - {username}",
    email=email,
    description=message_content
)
```

## Example: Weekly CEO Briefing

```python
# Generate weekly report
report = server.generate_business_report(days=7)

print(f"Revenue: {report['financial']['revenue']}")
print(f"Expenses: {report['financial']['expenses']}")
print(f"Profit: {report['financial']['profit']}")
print(f"Outstanding: {len(report['invoices']['outstanding'])}")
print(f"Active Leads: {len(report['leads'])}")
```

## Docker Integration

The Odoo MCP Server works with Docker-based Odoo:

```yaml
services:
  odoo:
    image: odoo:19
    ports:
      - "8069:8069"
    environment:
      - HOST=db
      - USER=odoo
      - PASSWORD=odoo
```

## Error Handling

The server includes comprehensive error handling:
- Connection retry logic
- Authentication validation
- API error logging
- Graceful degradation

## Security

- Uses XML-RPC over HTTPS
- Credentials stored in .env (not committed)
- Session management
- API rate limiting awareness

## Gold Tier Features

This skill is CRITICAL for Gold Tier:
- ✅ Odoo accounting integration (required)
- ✅ Business audit capabilities
- ✅ CEO briefing generation
- ✅ Cross-domain integration (Personal + Business)
- ✅ MCP server architecture

## Troubleshooting

### Connection Errors
- Verify Odoo URL is accessible
- Check database name
- Confirm user credentials
- Ensure XML-RPC is enabled

### Authentication Failed
- Verify username/password
- Check user has API access rights
- Confirm database exists

### Missing Data
- Install accounting module in Odoo
- Create sample invoices for testing
- Check date ranges in queries

## Next Steps

1. Set up Odoo instance (Docker recommended)
2. Configure accounting module
3. Test connection: `python odoo-mcp-server.py`
4. Integrate with CEO Briefing Generator
5. Set up automated weekly reports
6. Connect social media leads to CRM

---

*Part of Gold Tier AI Employee Implementation*
*Critical component for business automation*
*Built with Claude Code - March 2026*
