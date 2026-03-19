import os
import sys
import requests
from dotenv import load_dotenv

# Windows console encoding fix
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

# Facebook API Configuration
ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
PAGE_ID = os.getenv("FACEBOOK_PAGE_ID", "")
API_VERSION = "v21.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

def check_token_permissions():
    """Check what permissions the access token has"""
    print("\n" + "="*60)
    print("CHECKING ACCESS TOKEN PERMISSIONS")
    print("="*60)

    if not ACCESS_TOKEN:
        print("❌ ERROR: No access token found in .env file")
        print("   Add INSTAGRAM_ACCESS_TOKEN to your .env file")
        return False

    try:
        # Get token info
        response = requests.get(
            f"{BASE_URL}/me/permissions",
            params={'access_token': ACCESS_TOKEN}
        )
        response.raise_for_status()
        data = response.json()

        if 'data' not in data:
            print("❌ ERROR: Could not retrieve permissions")
            return False

        permissions = data['data']
        granted_permissions = [p['permission'] for p in permissions if p['status'] == 'granted']

        print(f"\n✓ Token is valid")
        print(f"✓ Found {len(granted_permissions)} granted permissions\n")

        # Required permissions for Facebook posting
        required_permissions = [
            'pages_show_list',
            'pages_read_engagement',
            'pages_manage_posts',
            'pages_manage_engagement'
        ]

        print("Required Permissions for Facebook Posting:")
        print("-" * 60)

        all_granted = True
        for perm in required_permissions:
            if perm in granted_permissions:
                print(f"  ✅ {perm}")
            else:
                print(f"  ❌ {perm} - MISSING!")
                all_granted = False

        print("\nAll Granted Permissions:")
        print("-" * 60)
        for perm in sorted(granted_permissions):
            print(f"  • {perm}")

        if all_granted:
            print("\n✅ SUCCESS: All required permissions are granted!")
            return True
        else:
            print("\n⚠️  WARNING: Some required permissions are missing!")
            print("\nTo fix this:")
            print("1. Go to https://developers.facebook.com/apps/")
            print("2. Select your app")
            print("3. Go to 'App Review' > 'Permissions and Features'")
            print("4. Request the missing permissions")
            print("5. Or regenerate token with correct permissions")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return False

def check_page_id():
    """Check if Page ID is configured and accessible"""
    print("\n" + "="*60)
    print("CHECKING FACEBOOK PAGE ID")
    print("="*60)

    if PAGE_ID:
        print(f"\n✓ Page ID found in .env: {PAGE_ID}")

        # Verify the Page ID is accessible
        try:
            response = requests.get(
                f"{BASE_URL}/{PAGE_ID}",
                params={
                    'fields': 'id,name,access_token',
                    'access_token': ACCESS_TOKEN
                }
            )
            response.raise_for_status()
            data = response.json()

            print(f"✅ Page is accessible!")
            print(f"   Name: {data.get('name', 'N/A')}")
            print(f"   ID: {data.get('id', 'N/A')}")

            # Check if we have a Page access token
            if 'access_token' in data:
                print(f"✅ Page access token available")
                return True, data.get('access_token')
            else:
                print(f"⚠️  No Page access token in response")
                return True, None

        except requests.exceptions.RequestException as e:
            print(f"❌ ERROR: Cannot access Page ID {PAGE_ID}")
            print(f"   {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"   Response: {e.response.text}")
            return False, None
    else:
        print("\n⚠️  No Page ID in .env file")
        print("   Attempting to auto-detect...")

        try:
            response = requests.get(
                f"{BASE_URL}/me/accounts",
                params={'access_token': ACCESS_TOKEN}
            )
            response.raise_for_status()
            data = response.json()

            if data and 'data' in data and len(data['data']) > 0:
                pages = data['data']
                print(f"\n✓ Found {len(pages)} Facebook Page(s):\n")

                for i, page in enumerate(pages, 1):
                    print(f"  {i}. {page.get('name', 'Unknown')}")
                    print(f"     ID: {page.get('id')}")
                    print(f"     Category: {page.get('category', 'N/A')}")
                    print()

                if len(pages) == 1:
                    page_id = pages[0]['id']
                    page_token = pages[0].get('access_token')
                    print(f"✅ Auto-detected Page ID: {page_id}")
                    print(f"\nAdd this to your .env file:")
                    print(f"FACEBOOK_PAGE_ID={page_id}")
                    return True, page_token
                else:
                    print("⚠️  Multiple pages found. Add the desired Page ID to .env:")
                    print(f"FACEBOOK_PAGE_ID=<your_page_id>")
                    return True, None
            else:
                print("❌ No Facebook Pages found")
                print("   Make sure you have a Facebook Page and admin access")
                return False, None

        except requests.exceptions.RequestException as e:
            print(f"❌ ERROR: {e}")
            return False, None

def test_post_capability(page_token=None):
    """Test if we can post to the Page"""
    print("\n" + "="*60)
    print("TESTING POST CAPABILITY")
    print("="*60)

    # Use Page token if available, otherwise use user token
    token = page_token if page_token else ACCESS_TOKEN

    if not PAGE_ID and not page_token:
        print("⚠️  Cannot test posting without Page ID")
        return False

    page_id = PAGE_ID
    if not page_id:
        # Try to get from auto-detection
        try:
            response = requests.get(
                f"{BASE_URL}/me/accounts",
                params={'access_token': ACCESS_TOKEN}
            )
            response.raise_for_status()
            data = response.json()
            if data and 'data' in data and len(data['data']) > 0:
                page_id = data['data'][0]['id']
        except:
            pass

    if not page_id:
        print("❌ No Page ID available for testing")
        return False

    print(f"\nTesting post capability for Page ID: {page_id}")
    print("(This is a dry-run test, no actual post will be created)\n")

    # Check if we can access the feed endpoint
    try:
        response = requests.get(
            f"{BASE_URL}/{page_id}/feed",
            params={
                'access_token': token,
                'limit': 1
            }
        )
        response.raise_for_status()

        print("✅ Can access Page feed endpoint")
        print("✅ Ready to post to Facebook!")
        return True

    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot access Page feed endpoint")
        print(f"   Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Response: {e.response.text}")
        return False

def main():
    """Run all checks"""
    print("\n" + "="*60)
    print("FACEBOOK INTEGRATION VERIFICATION")
    print("="*60)

    if not ACCESS_TOKEN:
        print("\n❌ CRITICAL: No access token found!")
        print("\nAdd to your .env file:")
        print("INSTAGRAM_ACCESS_TOKEN=your_token_here")
        sys.exit(1)

    # Check 1: Token permissions
    permissions_ok = check_token_permissions()

    # Check 2: Page ID
    page_ok, page_token = check_page_id()

    # Check 3: Post capability
    if permissions_ok and page_ok:
        post_ok = test_post_capability(page_token)
    else:
        post_ok = False

    # Final summary
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)

    print(f"\n1. Token Permissions: {'✅ PASS' if permissions_ok else '❌ FAIL'}")
    print(f"2. Page ID Setup: {'✅ PASS' if page_ok else '❌ FAIL'}")
    print(f"3. Post Capability: {'✅ PASS' if post_ok else '❌ FAIL'}")

    if permissions_ok and page_ok and post_ok:
        print("\n🎉 SUCCESS! Your Facebook integration is ready!")
        print("\nYou can now post to Facebook:")
        print("  python facebook-poster.py --post \"Your message here\"")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")

    print("\n" + "="*60)

if __name__ == "__main__":
    main()
