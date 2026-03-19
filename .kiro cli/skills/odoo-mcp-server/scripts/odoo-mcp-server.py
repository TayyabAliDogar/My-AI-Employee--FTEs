import os
import sys
import json
import xmlrpc.client
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

# Windows console encoding fix
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

# Odoo Configuration
ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_USER = os.getenv("ODOO_USER")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")

class OdooMCPServer:
    """MCP Server for Odoo Integration"""

    def __init__(self):
        self.url = ODOO_URL
        self.db = ODOO_DB
        self.username = ODOO_USER
        self.password = ODOO_PASSWORD
        self.uid = None
        self.models = None
        self.common = None

    def connect(self):
        """Establish connection to Odoo"""
        try:
            self.common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
            self.uid = self.common.authenticate(self.db, self.username, self.password, {})

            if self.uid:
                self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')
                print(f"✅ Connected to Odoo (User ID: {self.uid})")
                return True
            else:
                print("❌ Authentication failed")
                return False

        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False

    def execute(self, model, method, *args, **kwargs):
        """Execute Odoo model method"""
        if not self.uid or not self.models:
            if not self.connect():
                return None

        try:
            return self.models.execute_kw(
                self.db, self.uid, self.password,
                model, method, args, kwargs
            )
        except Exception as e:
            print(f"❌ Error executing {model}.{method}: {e}")
            return None

    # ==================== ACCOUNTING METHODS ====================

    def get_invoices(self, state=None, date_from=None, date_to=None, limit=100):
        """
        Get invoices from Odoo

        Args:
            state: Invoice state (draft, posted, cancel)
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)
            limit: Maximum number of records

        Returns:
            list: Invoice records
        """
        domain = []

        if state:
            domain.append(('state', '=', state))

        if date_from:
            domain.append(('invoice_date', '>=', date_from))

        if date_to:
            domain.append(('invoice_date', '<=', date_to))

        fields = [
            'name', 'partner_id', 'invoice_date', 'amount_total',
            'amount_untaxed', 'amount_tax', 'state', 'move_type',
            'payment_state', 'currency_id'
        ]

        invoices = self.execute('account.move', 'search_read', domain, {'fields': fields, 'limit': limit})
        return invoices

    def get_revenue(self, date_from=None, date_to=None):
        """
        Calculate total revenue from posted invoices

        Args:
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)

        Returns:
            dict: Revenue summary
        """
        invoices = self.get_invoices(state='posted', date_from=date_from, date_to=date_to)

        if not invoices:
            return {'total': 0, 'count': 0, 'currency': 'USD'}

        total_revenue = sum(inv['amount_total'] for inv in invoices if inv['move_type'] == 'out_invoice')
        currency = invoices[0]['currency_id'][1] if invoices and invoices[0].get('currency_id') else 'USD'

        return {
            'total': total_revenue,
            'count': len([inv for inv in invoices if inv['move_type'] == 'out_invoice']),
            'currency': currency,
            'invoices': invoices
        }

    def get_expenses(self, date_from=None, date_to=None):
        """
        Calculate total expenses from posted bills

        Args:
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)

        Returns:
            dict: Expense summary
        """
        invoices = self.get_invoices(state='posted', date_from=date_from, date_to=date_to)

        if not invoices:
            return {'total': 0, 'count': 0, 'currency': 'USD'}

        total_expenses = sum(inv['amount_total'] for inv in invoices if inv['move_type'] == 'in_invoice')
        currency = invoices[0]['currency_id'][1] if invoices and invoices[0].get('currency_id') else 'USD'

        return {
            'total': total_expenses,
            'count': len([inv for inv in invoices if inv['move_type'] == 'in_invoice']),
            'currency': currency,
            'bills': [inv for inv in invoices if inv['move_type'] == 'in_invoice']
        }

    def get_profit_loss(self, date_from=None, date_to=None):
        """
        Calculate profit/loss for a period

        Args:
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)

        Returns:
            dict: P&L summary
        """
        revenue = self.get_revenue(date_from, date_to)
        expenses = self.get_expenses(date_from, date_to)

        profit = revenue['total'] - expenses['total']

        return {
            'revenue': revenue['total'],
            'expenses': expenses['total'],
            'profit': profit,
            'margin': (profit / revenue['total'] * 100) if revenue['total'] > 0 else 0,
            'currency': revenue['currency'],
            'period': {
                'from': date_from,
                'to': date_to
            }
        }

    def get_customers(self, limit=100):
        """Get customer list"""
        domain = [('customer_rank', '>', 0)]
        fields = ['name', 'email', 'phone', 'country_id', 'total_invoiced']

        customers = self.execute('res.partner', 'search_read', domain, {'fields': fields, 'limit': limit})
        return customers

    def create_invoice(self, partner_id, invoice_lines, invoice_type='out_invoice'):
        """
        Create a new invoice

        Args:
            partner_id: Customer ID
            invoice_lines: List of invoice line dicts
            invoice_type: 'out_invoice' (customer) or 'in_invoice' (vendor)

        Returns:
            int: Invoice ID
        """
        invoice_data = {
            'partner_id': partner_id,
            'move_type': invoice_type,
            'invoice_line_ids': [(0, 0, line) for line in invoice_lines]
        }

        invoice_id = self.execute('account.move', 'create', invoice_data)
        return invoice_id

    def get_payments(self, date_from=None, date_to=None, limit=100):
        """Get payment records"""
        domain = [('payment_type', 'in', ['inbound', 'outbound'])]

        if date_from:
            domain.append(('date', '>=', date_from))

        if date_to:
            domain.append(('date', '<=', date_to))

        fields = ['name', 'partner_id', 'amount', 'date', 'payment_type', 'state', 'currency_id']

        payments = self.execute('account.payment', 'search_read', domain, {'fields': fields, 'limit': limit})
        return payments

    def get_outstanding_invoices(self):
        """Get unpaid invoices"""
        domain = [
            ('state', '=', 'posted'),
            ('payment_state', 'in', ['not_paid', 'partial'])
        ]

        fields = ['name', 'partner_id', 'invoice_date', 'invoice_date_due', 'amount_total', 'amount_residual']

        invoices = self.execute('account.move', 'search_read', domain, {'fields': fields})
        return invoices

    # ==================== CRM METHODS ====================

    def get_leads(self, stage=None, limit=100):
        """Get CRM leads"""
        domain = []

        if stage:
            domain.append(('stage_id.name', '=', stage))

        fields = ['name', 'partner_id', 'email_from', 'phone', 'expected_revenue', 'probability', 'stage_id']

        leads = self.execute('crm.lead', 'search_read', domain, {'fields': fields, 'limit': limit})
        return leads

    def create_lead(self, name, email=None, phone=None, description=None):
        """Create a new CRM lead"""
        lead_data = {
            'name': name,
            'type': 'opportunity'
        }

        if email:
            lead_data['email_from'] = email

        if phone:
            lead_data['phone'] = phone

        if description:
            lead_data['description'] = description

        lead_id = self.execute('crm.lead', 'create', lead_data)
        return lead_id

    # ==================== PRODUCT METHODS ====================

    def get_products(self, limit=100):
        """Get product list"""
        fields = ['name', 'list_price', 'standard_price', 'qty_available', 'categ_id']

        products = self.execute('product.product', 'search_read', [], {'fields': fields, 'limit': limit})
        return products

    # ==================== REPORTING METHODS ====================

    def generate_business_report(self, days=7):
        """
        Generate comprehensive business report

        Args:
            days: Number of days to include in report

        Returns:
            dict: Business metrics
        """
        date_to = datetime.now().strftime('%Y-%m-%d')
        date_from = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

        report = {
            'period': {
                'from': date_from,
                'to': date_to,
                'days': days
            },
            'financial': self.get_profit_loss(date_from, date_to),
            'invoices': {
                'outstanding': self.get_outstanding_invoices(),
                'recent': self.get_invoices(date_from=date_from, limit=10)
            },
            'payments': self.get_payments(date_from, date_to),
            'leads': self.get_leads(limit=10),
            'generated_at': datetime.now().isoformat()
        }

        return report

def main():
    """Main function for testing"""
    server = OdooMCPServer()

    if not server.connect():
        sys.exit(1)

    print("\n" + "=" * 60)
    print("ODOO MCP SERVER - TEST MODE")
    print("=" * 60)

    # Test: Get revenue
    print("\n📊 Revenue (Last 30 days):")
    date_from = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    revenue = server.get_revenue(date_from=date_from)
    print(f"  Total: {revenue['total']} {revenue['currency']}")
    print(f"  Invoices: {revenue['count']}")

    # Test: Get expenses
    print("\n💰 Expenses (Last 30 days):")
    expenses = server.get_expenses(date_from=date_from)
    print(f"  Total: {expenses['total']} {expenses['currency']}")
    print(f"  Bills: {expenses['count']}")

    # Test: Profit/Loss
    print("\n📈 Profit/Loss (Last 30 days):")
    pl = server.get_profit_loss(date_from=date_from)
    print(f"  Revenue: {pl['revenue']} {pl['currency']}")
    print(f"  Expenses: {pl['expenses']} {pl['currency']}")
    print(f"  Profit: {pl['profit']} {pl['currency']}")
    print(f"  Margin: {pl['margin']:.2f}%")

    # Test: Outstanding invoices
    print("\n⚠️  Outstanding Invoices:")
    outstanding = server.get_outstanding_invoices()
    print(f"  Count: {len(outstanding)}")
    if outstanding:
        total_outstanding = sum(inv['amount_residual'] for inv in outstanding)
        print(f"  Total Outstanding: {total_outstanding}")

    # Test: Recent leads
    print("\n🎯 Recent Leads:")
    leads = server.get_leads(limit=5)
    print(f"  Count: {len(leads)}")

    print("\n" + "=" * 60)
    print("✅ All tests completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
