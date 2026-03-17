#!/usr/bin/env python3
"""
Test LinkedIn Authentication with saved auth.json
"""

from playwright.sync_api import sync_playwright
import json

def test_linkedin_auth():
    print("Testing LinkedIn authentication...")

    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)

        # Create context with saved authentication
        context = browser.new_context(storage_state='auth.json')
        page = context.new_page()

        # Navigate to LinkedIn
        print("Navigating to LinkedIn...")
        page.goto('https://www.linkedin.com/feed/')

        # Wait a bit for page to load
        page.wait_for_timeout(3000)

        # Check if we're logged in by looking for the feed
        if 'feed' in page.url:
            print("✓ Successfully authenticated! You're logged in.")
            print(f"Current URL: {page.url}")
        else:
            print("✗ Authentication may have failed")
            print(f"Current URL: {page.url}")

        # Keep browser open for 5 seconds so you can see
        page.wait_for_timeout(5000)

        browser.close()
        print("Test complete!")

if __name__ == '__main__':
    test_linkedin_auth()
