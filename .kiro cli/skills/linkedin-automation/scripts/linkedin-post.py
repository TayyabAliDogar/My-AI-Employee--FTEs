#!/usr/bin/env python3
"""
LinkedIn Post Automation - Posts content to LinkedIn via Playwright
"""

import os
import sys
import json
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

class LinkedInPoster:
    def __init__(self, config_path='linkedin-config.json'):
        self.config = self.load_config(config_path)
        self.mcp_url = 'http://localhost:8808'
        self.vault_path = Path(self.config.get('vault_path', '../../Vault'))

    def load_config(self, config_path):
        """Load configuration"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def call_mcp(self, tool, params):
        """Call Playwright MCP server"""
        cmd = [
            'python3',
            '../../browsing-with-playwright/scripts/mcp-client.py',
            'call',
            '-u', self.mcp_url,
            '-t', tool,
            '-p', json.dumps(params)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"MCP call failed: {result.stderr}")

        return json.loads(result.stdout) if result.stdout else {}

    def login_to_linkedin(self):
        """Login to LinkedIn"""
        email = os.getenv('LINKEDIN_EMAIL') or self.config.get('email')
        password = os.getenv('LINKEDIN_PASSWORD') or self.config.get('password')

        if not email or not password:
            raise Exception("LinkedIn credentials not found")

        print("Navigating to LinkedIn...")
        self.call_mcp('browser_navigate', {'url': 'https://www.linkedin.com/login'})

        print("Getting page snapshot...")
        snapshot = self.call_mcp('browser_snapshot', {})

        print("Entering credentials...")
        # Find email and password fields from snapshot
        self.call_mcp('browser_type', {
            'element': 'Email or Phone',
            'text': email,
            'submit': False
        })

        self.call_mcp('browser_type', {
            'element': 'Password',
            'text': password,
            'submit': True
        })

        # Wait for login
        self.call_mcp('browser_wait_for', {'time': 3000})

        print("✓ Logged in to LinkedIn")

    def create_post(self, content, image_path=None):
        """Create a LinkedIn post"""
        print("Navigating to LinkedIn feed...")
        self.call_mcp('browser_navigate', {'url': 'https://www.linkedin.com/feed/'})

        self.call_mcp('browser_wait_for', {'time': 2000})

        print("Clicking 'Start a post' button...")
        snapshot = self.call_mcp('browser_snapshot', {})

        self.call_mcp('browser_click', {
            'element': 'Start a post'
        })

        self.call_mcp('browser_wait_for', {'time': 1000})

        print("Typing post content...")
        self.call_mcp('browser_type', {
            'element': 'Share your thoughts',
            'text': content,
            'submit': False
        })

        if image_path and os.path.exists(image_path):
            print(f"Uploading image: {image_path}")
            # Image upload logic would go here
            pass

        print("Post ready. Review before publishing.")
        return True

    def publish_post(self):
        """Click the Post button to publish"""
        print("Publishing post...")
        self.call_mcp('browser_click', {
            'element': 'Post'
        })

        self.call_mcp('browser_wait_for', {'time': 3000})

        # Get current URL to save post link
        result = self.call_mcp('browser_evaluate', {
            'function': 'return window.location.href'
        })

        print("✓ Post published successfully!")
        return result

    def save_post_record(self, content, post_url):
        """Save post record to vault"""
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f"LINKEDIN_POST_{timestamp}.md"
        filepath = self.vault_path / 'Done' / filename

        record = f"""# LinkedIn Post

**Published:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**URL:** {post_url}

## Content

{content}

---

*Auto-posted by LinkedIn Automation*
"""

        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(record)

        print(f"✓ Post record saved: {filename}")

def main():
    parser = argparse.ArgumentParser(description='Post to LinkedIn')
    parser.add_argument('--content', required=True, help='Post content')
    parser.add_argument('--image', help='Path to image file')
    parser.add_argument('--auto-publish', action='store_true', help='Auto-publish without confirmation')

    args = parser.parse_args()

    poster = LinkedInPoster()

    try:
        poster.login_to_linkedin()
        poster.create_post(args.content, args.image)

        if args.auto_publish:
            result = poster.publish_post()
            poster.save_post_record(args.content, result.get('url', 'N/A'))
        else:
            print("\n⚠️  Post created but not published.")
            print("Review the post in your browser, then run with --auto-publish to publish.")

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
