import os
import sys
import json
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import base64
import hmac
import hashlib
import time
import urllib.parse

# Windows console encoding fix
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

# Twitter API Configuration
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "")
API_KEY = os.getenv("TWITTER_API_KEY", "")
API_SECRET = os.getenv("TWITTER_API_SECRET", "")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN", "")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "")
API_VERSION = "2"
BASE_URL = f"https://api.twitter.com/{API_VERSION}"

def create_oauth1_header(method, url, params=None):
    """Create OAuth 1.0a header for Twitter API v2"""
    if params is None:
        params = {}

    oauth_params = {
        'oauth_consumer_key': API_KEY,
        'oauth_token': ACCESS_TOKEN,
        'oauth_signature_method': 'HMAC-SHA1',
        'oauth_timestamp': str(int(time.time())),
        'oauth_nonce': base64.b64encode(os.urandom(32)).decode('utf-8'),
        'oauth_version': '1.0'
    }

    # Combine all parameters
    all_params = {**params, **oauth_params}

    # Create signature base string
    sorted_params = sorted(all_params.items())
    param_string = '&'.join([f"{k}={urllib.parse.quote(str(v), safe='')}" for k, v in sorted_params])
    base_string = f"{method}&{urllib.parse.quote(url, safe='')}&{urllib.parse.quote(param_string, safe='')}"

    # Create signing key
    signing_key = f"{urllib.parse.quote(API_SECRET, safe='')}&{urllib.parse.quote(ACCESS_TOKEN_SECRET, safe='')}"

    # Generate signature
    signature = base64.b64encode(
        hmac.new(signing_key.encode(), base_string.encode(), hashlib.sha1).digest()
    ).decode()

    oauth_params['oauth_signature'] = signature

    # Create header
    header_params = ', '.join([f'{k}="{urllib.parse.quote(str(v), safe="")}"' for k, v in sorted(oauth_params.items())])
    return f"OAuth {header_params}"

def post_tweet(text, reply_to_id=None):
    """
    Post a tweet

    Args:
        text: Tweet text (max 280 characters)
        reply_to_id: Optional tweet ID to reply to

    Returns:
        dict: Response from Twitter API
    """
    try:
        endpoint = f"{BASE_URL}/tweets"

        payload = {"text": text}
        if reply_to_id:
            payload["reply"] = {"in_reply_to_tweet_id": reply_to_id}

        headers = {
            'Authorization': f'Bearer {BEARER_TOKEN}',
            'Content-Type': 'application/json'
        }

        print(f"Posting tweet...")
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if 'data' in data and 'id' in data['data']:
            tweet_id = data['data']['id']
            print(f"✅ Successfully posted tweet!")
            print(f"Tweet ID: {tweet_id}")
            print(f"URL: https://twitter.com/i/web/status/{tweet_id}")
            return data
        else:
            print(f"❌ Failed to post tweet: {data}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Error posting tweet: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None

def delete_tweet(tweet_id):
    """
    Delete a tweet

    Args:
        tweet_id: ID of the tweet to delete

    Returns:
        dict: Response from Twitter API
    """
    try:
        endpoint = f"{BASE_URL}/tweets/{tweet_id}"

        headers = {
            'Authorization': f'Bearer {BEARER_TOKEN}'
        }

        print(f"Deleting tweet {tweet_id}...")
        response = requests.delete(endpoint, headers=headers)
        response.raise_for_status()
        data = response.json()

        if 'data' in data and data['data'].get('deleted'):
            print(f"✅ Successfully deleted tweet!")
            return data
        else:
            print(f"❌ Failed to delete tweet: {data}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Error deleting tweet: {e}")
        return None

def like_tweet(tweet_id):
    """
    Like a tweet

    Args:
        tweet_id: ID of the tweet to like

    Returns:
        dict: Response from Twitter API
    """
    try:
        # Get user ID first
        me_response = requests.get(
            f"{BASE_URL}/users/me",
            headers={'Authorization': f'Bearer {BEARER_TOKEN}'}
        )
        me_response.raise_for_status()
        user_id = me_response.json()['data']['id']

        endpoint = f"{BASE_URL}/users/{user_id}/likes"

        headers = {
            'Authorization': f'Bearer {BEARER_TOKEN}',
            'Content-Type': 'application/json'
        }

        payload = {"tweet_id": tweet_id}

        print(f"Liking tweet {tweet_id}...")
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if 'data' in data and data['data'].get('liked'):
            print(f"✅ Successfully liked tweet!")
            return data
        else:
            print(f"❌ Failed to like tweet: {data}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Error liking tweet: {e}")
        return None

def retweet(tweet_id):
    """
    Retweet a tweet

    Args:
        tweet_id: ID of the tweet to retweet

    Returns:
        dict: Response from Twitter API
    """
    try:
        # Get user ID first
        me_response = requests.get(
            f"{BASE_URL}/users/me",
            headers={'Authorization': f'Bearer {BEARER_TOKEN}'}
        )
        me_response.raise_for_status()
        user_id = me_response.json()['data']['id']

        endpoint = f"{BASE_URL}/users/{user_id}/retweets"

        headers = {
            'Authorization': f'Bearer {BEARER_TOKEN}',
            'Content-Type': 'application/json'
        }

        payload = {"tweet_id": tweet_id}

        print(f"Retweeting {tweet_id}...")
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if 'data' in data and data['data'].get('retweeted'):
            print(f"✅ Successfully retweeted!")
            return data
        else:
            print(f"❌ Failed to retweet: {data}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Error retweeting: {e}")
        return None

def get_user_info():
    """Get authenticated user information"""
    try:
        endpoint = f"{BASE_URL}/users/me"
        params = {
            "user.fields": "created_at,description,public_metrics,verified"
        }

        headers = {
            'Authorization': f'Bearer {BEARER_TOKEN}'
        }

        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if 'data' in data:
            user = data['data']
            print("📊 Twitter Account Info:")
            print(f"  Username: @{user.get('username', 'N/A')}")
            print(f"  Name: {user.get('name', 'N/A')}")
            print(f"  Followers: {user.get('public_metrics', {}).get('followers_count', 'N/A')}")
            print(f"  Following: {user.get('public_metrics', {}).get('following_count', 'N/A')}")
            print(f"  Tweets: {user.get('public_metrics', {}).get('tweet_count', 'N/A')}")
            print(f"  Verified: {user.get('verified', False)}")
            return data

        return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching user info: {e}")
        return None

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Twitter Poster for AI Employee")
    parser.add_argument('--tweet', type=str, help='Post a tweet')
    parser.add_argument('--reply', type=str, help='Reply to tweet (provide tweet ID)')
    parser.add_argument('--message', type=str, help='Reply message')
    parser.add_argument('--delete', type=str, help='Delete tweet (provide tweet ID)')
    parser.add_argument('--like', type=str, help='Like tweet (provide tweet ID)')
    parser.add_argument('--retweet', type=str, help='Retweet (provide tweet ID)')
    parser.add_argument('--info', action='store_true', help='Get account information')

    args = parser.parse_args()

    if not BEARER_TOKEN:
        print("❌ ERROR: Twitter Bearer Token not found in .env file")
        sys.exit(1)

    if args.tweet:
        if len(args.tweet) > 280:
            print("❌ ERROR: Tweet exceeds 280 characters")
            sys.exit(1)
        post_tweet(args.tweet)

    elif args.reply:
        if not args.message:
            print("❌ ERROR: --message is required when replying")
            sys.exit(1)
        if len(args.message) > 280:
            print("❌ ERROR: Reply exceeds 280 characters")
            sys.exit(1)
        post_tweet(args.message, reply_to_id=args.reply)

    elif args.delete:
        delete_tweet(args.delete)

    elif args.like:
        like_tweet(args.like)

    elif args.retweet:
        retweet(args.retweet)

    elif args.info:
        get_user_info()

    else:
        print("❌ ERROR: Please specify an action")
        parser.print_help()
        sys.exit(1)
