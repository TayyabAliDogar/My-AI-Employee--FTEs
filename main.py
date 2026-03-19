import os
import sys
from dotenv import load_dotenv
import xmlrpc.client

# Windows console encoding fix
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# .env file se data load karna
load_dotenv()

# Odoo Details
url = os.getenv("ODOO_URL")
db = os.getenv("ODOO_DB")
username = os.getenv("ODOO_USER")
password = os.getenv("ODOO_PASSWORD")

def connect_odoo():
    try:
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        uid = common.authenticate(db, username, password, {})
        if uid:
            print(f"✅ Odoo se connection kamyab! User ID: {uid}")
            return uid
        else:
            print("❌ Login fail ho gaya. Credentials check karein.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    connect_odoo()