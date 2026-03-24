#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Token Refresh Helper
Run this to get a new Instagram access token for the demo
"""

import webbrowser
import time

print("=" * 80)
print("INSTAGRAM TOKEN REFRESH HELPER")
print("=" * 80)
print()
print("Follow these steps to refresh your Instagram access token:")
print()
print("1. Opening Facebook Graph API Explorer in your browser...")
time.sleep(2)

# Open Graph API Explorer
webbrowser.open("https://developers.facebook.com/tools/explorer/")

print()
print("2. In the Graph API Explorer:")
print("   - Select your app: 'My personal AI employee'")
print("   - Click 'Generate Access Token'")
print("   - Make sure these permissions are checked:")
print("     * instagram_basic")
print("     * instagram_content_publish")
print("     * instagram_manage_messages")
print("     * pages_show_list")
print("     * pages_manage_posts")
print()
print("3. Copy the new access token")
print()
print("4. Update your .env file:")
print("   INSTAGRAM_ACCESS_TOKEN=<paste_new_token_here>")
print()
print("5. Get the page access token:")
print("   - In Graph API Explorer, enter: me/accounts")
print("   - Click Submit")
print("   - Copy the 'access_token' from the response")
print("   - Update .env:")
print("   FACEBOOK_ACCESS_TOKEN=<paste_page_token_here>")
print()
print("6. Save .env and run: python demo-master.py")
print()
print("=" * 80)
print("Press Ctrl+C to exit")
print("=" * 80)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n\nDone! Update your .env file and run the demo.")
