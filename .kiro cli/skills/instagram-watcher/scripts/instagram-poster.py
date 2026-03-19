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

# Instagram API Configuration
ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID")
API_VERSION = "v21.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

def post_to_instagram(image_url, caption):
    """
    Post an image to Instagram

    Args:
        image_url: URL of the image to post
        caption: Caption for the post

    Returns:
        dict: Response from Instagram API
    """
    try:
        # Step 1: Create media container
        container_endpoint = f"{BASE_URL}/{ACCOUNT_ID}/media"
        container_params = {
            'image_url': image_url,
            'caption': caption,
            'access_token': ACCESS_TOKEN
        }

        print(f"Creating media container...")
        container_response = requests.post(container_endpoint, data=container_params)
        container_response.raise_for_status()
        container_data = container_response.json()

        if 'id' not in container_data:
            print(f"❌ Failed to create container: {container_data}")
            return None

        container_id = container_data['id']
        print(f"✓ Container created: {container_id}")

        # Step 2: Publish the media
        publish_endpoint = f"{BASE_URL}/{ACCOUNT_ID}/media_publish"
        publish_params = {
            'creation_id': container_id,
            'access_token': ACCESS_TOKEN
        }

        print(f"Publishing media...")
        publish_response = requests.post(publish_endpoint, data=publish_params)
        publish_response.raise_for_status()
        publish_data = publish_response.json()

        if 'id' in publish_data:
            print(f"✅ Successfully posted to Instagram!")
            print(f"Post ID: {publish_data['id']}")
            return publish_data
        else:
            print(f"❌ Failed to publish: {publish_data}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Error posting to Instagram: {e}")
        return None

def post_story(image_url):
    """
    Post a story to Instagram

    Args:
        image_url: URL of the image for the story

    Returns:
        dict: Response from Instagram API
    """
    try:
        endpoint = f"{BASE_URL}/{ACCOUNT_ID}/media"
        params = {
            'image_url': image_url,
            'media_type': 'STORIES',
            'access_token': ACCESS_TOKEN
        }

        print(f"Creating story container...")
        container_response = requests.post(endpoint, data=params)
        container_response.raise_for_status()
        container_data = container_response.json()

        if 'id' not in container_data:
            print(f"❌ Failed to create story container: {container_data}")
            return None

        container_id = container_data['id']

        # Publish story
        publish_endpoint = f"{BASE_URL}/{ACCOUNT_ID}/media_publish"
        publish_params = {
            'creation_id': container_id,
            'access_token': ACCESS_TOKEN
        }

        print(f"Publishing story...")
        publish_response = requests.post(publish_endpoint, data=publish_params)
        publish_response.raise_for_status()
        publish_data = publish_response.json()

        if 'id' in publish_data:
            print(f"✅ Successfully posted story to Instagram!")
            print(f"Story ID: {publish_data['id']}")
            return publish_data
        else:
            print(f"❌ Failed to publish story: {publish_data}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Error posting story: {e}")
        return None

def reply_to_comment(comment_id, message):
    """
    Reply to an Instagram comment

    Args:
        comment_id: ID of the comment to reply to
        message: Reply message

    Returns:
        dict: Response from Instagram API
    """
    try:
        endpoint = f"{BASE_URL}/{comment_id}/replies"
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

def get_account_insights():
    """
    Get Instagram account insights

    Returns:
        dict: Account insights data
    """
    try:
        endpoint = f"{BASE_URL}/{ACCOUNT_ID}/insights"
        params = {
            'metric': 'impressions,reach,profile_views,follower_count',
            'period': 'day',
            'access_token': ACCESS_TOKEN
        }

        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()

        print("📊 Instagram Account Insights:")
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

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Instagram Poster for AI Employee")
    parser.add_argument('--post', type=str, help='Post image (provide image URL)')
    parser.add_argument('--caption', type=str, help='Caption for the post')
    parser.add_argument('--story', type=str, help='Post story (provide image URL)')
    parser.add_argument('--reply', type=str, help='Reply to comment (provide comment ID)')
    parser.add_argument('--message', type=str, help='Reply message')
    parser.add_argument('--insights', action='store_true', help='Get account insights')

    args = parser.parse_args()

    if not ACCESS_TOKEN or not ACCOUNT_ID:
        print("❌ ERROR: Instagram credentials not found in .env file")
        sys.exit(1)

    if args.post:
        if not args.caption:
            print("❌ ERROR: --caption is required when posting")
            sys.exit(1)
        post_to_instagram(args.post, args.caption)

    elif args.story:
        post_story(args.story)

    elif args.reply:
        if not args.message:
            print("❌ ERROR: --message is required when replying")
            sys.exit(1)
        reply_to_comment(args.reply, args.message)

    elif args.insights:
        get_account_insights()

    else:
        print("❌ ERROR: Please specify an action (--post, --story, --reply, or --insights)")
        parser.print_help()
        sys.exit(1)
