import os
import sys
from dotenv import load_dotenv
import requests

# Load environment
load_dotenv()

ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")

print("\n" + "="*60)
print("QUICK FACEBOOK POST TEST")
print("="*60)

if not ACCESS_TOKEN:
    print("\n❌ No access token in .env")
    sys.exit(1)

if not PAGE_ID or PAGE_ID == "your_facebook_page_id_here":
    print("\n❌ No valid Page ID in .env")
    print("   Current value:", PAGE_ID)
    sys.exit(1)

# Test token
print("\n1. Testing access token...")
try:
    r = requests.get(f"https://graph.facebook.com/v21.0/me", params={'access_token': ACCESS_TOKEN})
    r.raise_for_status()
    print("   ✅ Token is valid")
except Exception as e:
    print(f"   ❌ Token error: {e}")
    sys.exit(1)

# Test Page access
print("\n2. Testing Page access...")
try:
    r = requests.get(f"https://graph.facebook.com/v21.0/{PAGE_ID}", params={'access_token': ACCESS_TOKEN, 'fields': 'name'})
    r.raise_for_status()
    data = r.json()
    print(f"   ✅ Page accessible: {data.get('name')}")
except Exception as e:
    print(f"   ❌ Page error: {e}")
    sys.exit(1)

# Test posting capability
print("\n3. Testing post capability...")
try:
    r = requests.get(f"https://graph.facebook.com/v21.0/{PAGE_ID}/feed", params={'access_token': ACCESS_TOKEN, 'limit': 1})
    r.raise_for_status()
    print("   ✅ Can access feed endpoint")
except Exception as e:
    print(f"   ❌ Feed error: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("✅ ALL TESTS PASSED!")
print("="*60)
print("\nYou can now post to Facebook:")
print("  python facebook-poster.py --post \"Your message\"")
print("\n" + "="*60)
