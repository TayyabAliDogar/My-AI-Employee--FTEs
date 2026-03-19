import os
import sys
import json
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Windows console encoding fix
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

# Facebook API Configuration
ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")  # Same token works for Facebook
PAGE_ID = os.getenv("FACEBOOK_PAGE_ID", "")
API_VERSION = "v21.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

def get_page_id():
    """Get Facebook Page ID from access token"""
    global PAGE_ID
    if PAGE_ID:
        return PAGE_ID

    try:
        response = requests.get(
            f"{BASE_URL}/me/accounts",
            params={'access_token': ACCESS_TOKEN}
        )
        response.raise_for_status()
        data = response.json()

        if data and 'data' in data and len(data['data']) > 0:
            PAGE_ID = data['data'][0]['id']
            print(f"✓ Using Page ID: {PAGE_ID}")
            return PAGE_ID

        print("❌ No Facebook Page found")
        return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Error getting Page ID: {e}")
        return None

def post_to_facebook(message, link=None, image_url=None):
    """
    Post a message to Facebook Page

    Args:
        message: Text content of the post
        link: Optional URL to include
        image_url: Optional image URL

    Returns:
        dict: Response from Facebook API
    """
    page_id = get_page_id()
    if not page_id:
        return None

    try:
        endpoint = f"{BASE_URL}/{page_id}/feed"
        params = {
            'message': message,
            'access_token': ACCESS_TOKEN
        }

        if link:
            params['link'] = link

        if image_url:
            # For images, use photos endpoint
            endpoint = f"{BASE_URL}/{page_id}/photos"
            params['url'] = image_url
            params['caption'] = message

        print(f"Posting to Facebook...")
        response = requests.post(endpoint, data=params)
        response.raise_for_status()
        data = response.json()

        if 'id' in data:
            print(f"✅ Successfully posted to Facebook!")
            print(f"Post ID: {data['id']}")
            return data
        else:
            print(f"❌ Failed to post: {data}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Error posting to Facebook: {e}")
        return None

def reply_to_comment(comment_id, message):
    """
    Reply to a Facebook comment

    Args:
        comment_id: ID of the comment to reply to
        message: Reply message

    Returns:
        dict: Response from Facebook API
    """
    try:
        endpoint = f"{BASE_URL}/{comment_id}/comments"
        params = {
            'message': message,
            'access_token': ACCESS_TOKEN
        }

        print(f"Replying to comment {comment_id}...")
        response = requests.post(endpoint, data=params)
        response.raise_for_status()
        data = response.json()

        if 'id' in data:
            print(f"✅ Successfully replied to comment!")
            print(f"Reply ID: {data['id']}")
            return data
        else:
            print(f"❌ Failed to reply: {data}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Error replying to comment: {e}")
        return None

def send_message(recipient_id, message):
    """
    Send a private message via Facebook Messenger

    Args:
        recipient_id: ID of the recipient
        message: Message text

    Returns:
        dict: Response from Facebook API
    """
    page_id = get_page_id()
    if not page_id:
        return None

    try:
        endpoint = f"{BASE_URL}/{page_id}/messages"
        params = {
            'recipient': json.dumps({'id': recipient_id}),
            'message': json.dumps({'text': message}),
            'access_token': ACCESS_TOKEN
        }

        print(f"Sending message to {recipient_id}...")
        response = requests.post(endpoint, data=params)
        response.raise_for_status()
        data = response.json()

        if 'message_id' in data:
            print(f"✅ Successfully sent message!")
            print(f"Message ID: {data['message_id']}")
            return data
        else:
            print(f"❌ Failed to send message: {data}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending message: {e}")
        return None

def get_page_insights():
    """
    Get Facebook Page insights

    Returns:
        dict: Page insights data
    """
    page_id = get_page_id()
    if not page_id:
        return None

    try:
        endpoint = f"{BASE_URL}/{page_id}/insights"
        params = {
            'metric': 'page_impressions,page_engaged_users,page_post_engagements,page_fans',
            'period': 'day',
            'access_token': ACCESS_TOKEN
        }

        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()

        print("📊 Facebook Page Insights:")
        if 'data' in data:
            for metric in data['data']:
                name = metric.get('name', 'Unknown')
                values = metric.get('values', [])
                if values:
                    value = values[0].get('value', 'N/A')
                    print(f"  {name}: {value}")

        return data

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching insights: {e}")
        return None

def get_page_info():
    """Get Facebook Page information"""
    page_id = get_page_id()
    if not page_id:
        return None

    try:
        endpoint = f"{BASE_URL}/{page_id}"
        params = {
            'fields': 'id,name,fan_count,followers_count,about,category',
            'access_token': ACCESS_TOKEN
        }

        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()

        print("📄 Facebook Page Info:")
        print(f"  Name: {data.get('name', 'N/A')}")
        print(f"  Category: {data.get('category', 'N/A')}")
        print(f"  Fans: {data.get('fan_count', 'N/A')}")
        print(f"  Followers: {data.get('followers_count', 'N/A')}")

        return data

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching page info: {e}")
        return None

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Facebook Poster for AI Employee")
    parser.add_argument('--post', type=str, help='Post message to Facebook')
    parser.add_argument('--link', type=str, help='Link to include in post')
    parser.add_argument('--image', type=str, help='Image URL to post')
    parser.add_argument('--reply', type=str, help='Reply to comment (provide comment ID)')
    parser.add_argument('--message', type=str, help='Message text for reply or DM')
    parser.add_argument('--send', type=str, help='Send DM (provide recipient ID)')
    parser.add_argument('--insights', action='store_true', help='Get page insights')
    parser.add_argument('--info', action='store_true', help='Get page information')

    args = parser.parse_args()

    if not ACCESS_TOKEN:
        print("❌ ERROR: Facebook access token not found in .env file")
        sys.exit(1)

    if args.post:
        post_to_facebook(args.post, link=args.link, image_url=args.image)

    elif args.reply:
        if not args.message:
            print("❌ ERROR: --message is required when replying")
            sys.exit(1)
        reply_to_comment(args.reply, args.message)

    elif args.send:
        if not args.message:
            print("❌ ERROR: --message is required when sending DM")
            sys.exit(1)
        send_message(args.send, args.message)

    elif args.insights:
        get_page_insights()

    elif args.info:
        get_page_info()

    else:
        print("❌ ERROR: Please specify an action")
        parser.print_help()
        sys.exit(1)
