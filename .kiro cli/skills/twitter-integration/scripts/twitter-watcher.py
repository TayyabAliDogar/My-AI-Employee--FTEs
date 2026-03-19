import os
import sys
import json
import time
import requests
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

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

# Paths
SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "twitter-config.json"
VAULT_DIR = Path(__file__).parent.parent.parent.parent / "Vault"
NEEDS_ACTION_DIR = VAULT_DIR / "Needs_Action"
DONE_DIR = VAULT_DIR / "Done"
LOGS_DIR = VAULT_DIR / "Logs"

# Create directories
NEEDS_ACTION_DIR.mkdir(parents=True, exist_ok=True)
DONE_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

def load_config():
    """Load configuration from JSON file"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "check_interval": 300,
        "monitor_mentions": True,
        "monitor_dms": True,
        "priority_keywords": ["urgent", "asap", "important", "help"],
        "categories": {
            "customer_inquiry": ["price", "cost", "buy", "purchase"],
            "support": ["help", "issue", "problem", "not working"],
            "feedback": ["love", "great", "terrible", "bad"],
            "lead": ["interested", "more info", "contact"]
        },
        "track_keywords": []
    }

def save_config(config):
    """Save configuration to JSON file"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)

def log_message(message, level="INFO"):
    """Log message to file and console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}"
    print(log_entry)

    log_file = LOGS_DIR / f"twitter-watcher-{datetime.now().strftime('%Y-%m-%d')}.log"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry + "\n")

def make_api_request(endpoint, params=None, method='GET'):
    """Make request to Twitter API v2"""
    if params is None:
        params = {}

    headers = {
        'Authorization': f'Bearer {BEARER_TOKEN}',
        'Content-Type': 'application/json'
    }

    try:
        url = f"{BASE_URL}/{endpoint}"
        if method == 'GET':
            response = requests.get(url, headers=headers, params=params)
        else:
            response = requests.post(url, headers=headers, json=params)

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        log_message(f"API request failed: {e}", "ERROR")
        return None

def get_user_id():
    """Get authenticated user's Twitter ID"""
    data = make_api_request("users/me")
    if data and 'data' in data:
        user_id = data['data']['id']
        username = data['data']['username']
        log_message(f"Authenticated as @{username} (ID: {user_id})")
        return user_id, username
    return None, None

def get_mentions(user_id, since_id=None):
    """Fetch mentions of the authenticated user"""
    endpoint = f"users/{user_id}/mentions"
    params = {
        "tweet.fields": "created_at,author_id,conversation_id,in_reply_to_user_id",
        "expansions": "author_id",
        "user.fields": "username,name",
        "max_results": 10
    }

    if since_id:
        params['since_id'] = since_id

    data = make_api_request(endpoint, params)
    if data and 'data' in data:
        return data['data'], data.get('includes', {})
    return [], {}

def search_tweets(query, max_results=10):
    """Search for tweets matching a query"""
    endpoint = "tweets/search/recent"
    params = {
        "query": query,
        "tweet.fields": "created_at,author_id,conversation_id",
        "expansions": "author_id",
        "user.fields": "username,name",
        "max_results": max_results
    }

    data = make_api_request(endpoint, params)
    if data and 'data' in data:
        return data['data'], data.get('includes', {})
    return [], {}

def categorize_content(text, config):
    """Categorize content based on keywords"""
    if not text:
        return ["general"]

    text_lower = text.lower()
    categories = []

    for category, keywords in config['categories'].items():
        if any(keyword in text_lower for keyword in keywords):
            categories.append(category)

    return categories if categories else ["general"]

def detect_priority(text, config):
    """Detect if content is high priority"""
    if not text:
        return "NORMAL"

    text_lower = text.lower()
    for keyword in config['priority_keywords']:
        if keyword in text_lower:
            return "HIGH"
    return "NORMAL"

def get_user_info(users_data, author_id):
    """Extract user info from includes data"""
    if 'users' in users_data:
        for user in users_data['users']:
            if user['id'] == author_id:
                return user.get('username', 'Unknown'), user.get('name', 'Unknown')
    return 'Unknown', 'Unknown'

def create_action_file(item_type, content, metadata):
    """Create action file in Vault/Needs_Action/"""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    from_user = metadata.get('from', 'unknown').replace(' ', '_').replace('@', '')
    filename = f"TWITTER_{item_type}_{from_user}_{timestamp}.md"
    filepath = NEEDS_ACTION_DIR / filename

    categories = ", ".join(metadata.get('categories', ['general']))
    priority = metadata.get('priority', 'NORMAL')

    action_content = f"""# TWITTER {item_type.upper()}: {metadata.get('subject', 'New Interaction')}

**From:** @{metadata.get('from', 'Unknown')}
**Name:** {metadata.get('name', 'Unknown')}
**Type:** {item_type}
**Category:** {categories}
**Priority:** {priority}
**Timestamp:** {metadata.get('timestamp', datetime.now().isoformat())}
**Tweet ID:** {metadata.get('tweet_id', 'N/A')}
**URL:** {metadata.get('url', 'N/A')}

## Content

{content}

## Suggested Actions

- [ ] Review {item_type}
- [ ] Respond if needed
- [ ] Update CRM/Odoo
- [ ] Mark as done

## Metadata

```json
{json.dumps(metadata, indent=2)}
```

---
*Generated by Twitter Watcher - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(action_content)

    log_message(f"✓ Created action file: {filename}")
    return filepath

def process_mentions(config, user_id, since_id=None):
    """Process Twitter mentions"""
    if not config.get('monitor_mentions', True):
        return 0, None

    log_message("Fetching Twitter mentions...")
    mentions, includes = get_mentions(user_id, since_id)

    processed_count = 0
    latest_id = since_id

    for mention in mentions:
        tweet_text = mention.get('text', '')
        if not tweet_text:
            continue

        tweet_id = mention.get('id')
        author_id = mention.get('author_id')
        username, name = get_user_info(includes, author_id)

        categories = categorize_content(tweet_text, config)
        priority = detect_priority(tweet_text, config)

        metadata = {
            'from': username,
            'name': name,
            'tweet_id': tweet_id,
            'author_id': author_id,
            'conversation_id': mention.get('conversation_id'),
            'timestamp': mention.get('created_at'),
            'categories': categories,
            'priority': priority,
            'subject': f"Mention from @{username}",
            'url': f"https://twitter.com/{username}/status/{tweet_id}"
        }

        create_action_file("MENTION", tweet_text, metadata)
        processed_count += 1

        # Track latest ID for next check
        if not latest_id or int(tweet_id) > int(latest_id):
            latest_id = tweet_id

    return processed_count, latest_id

def process_keyword_tracking(config):
    """Process keyword tracking"""
    keywords = config.get('track_keywords', [])
    if not keywords:
        return 0

    log_message(f"Tracking keywords: {', '.join(keywords)}")
    processed_count = 0

    for keyword in keywords:
        tweets, includes = search_tweets(keyword, max_results=5)

        for tweet in tweets:
            tweet_text = tweet.get('text', '')
            if not tweet_text:
                continue

            tweet_id = tweet.get('id')
            author_id = tweet.get('author_id')
            username, name = get_user_info(includes, author_id)

            categories = [f"keyword:{keyword}"]
            priority = "NORMAL"

            metadata = {
                'from': username,
                'name': name,
                'tweet_id': tweet_id,
                'author_id': author_id,
                'keyword': keyword,
                'timestamp': tweet.get('created_at'),
                'categories': categories,
                'priority': priority,
                'subject': f"Keyword match: {keyword}",
                'url': f"https://twitter.com/{username}/status/{tweet_id}"
            }

            create_action_file("KEYWORD", tweet_text, metadata)
            processed_count += 1

    return processed_count

def generate_summary():
    """Generate daily summary of Twitter activity"""
    log_message("Generating Twitter activity summary...")

    # Count action files
    action_files = list(NEEDS_ACTION_DIR.glob("TWITTER_*.md"))
    done_files = list(DONE_DIR.glob("TWITTER_*.md"))

    summary = f"""# Twitter Activity Summary
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Statistics
- Pending Actions: {len(action_files)}
- Completed Actions: {len(done_files)}
- Total Interactions: {len(action_files) + len(done_files)}

## Pending Actions
"""

    for action_file in action_files[:10]:  # Show first 10
        summary += f"- {action_file.name}\n"

    summary_file = LOGS_DIR / f"twitter-summary-{datetime.now().strftime('%Y-%m-%d')}.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary)

    log_message(f"✓ Summary saved: {summary_file.name}")
    return summary_file

def watch_twitter(once=False):
    """Main watcher loop"""
    config = load_config()
    save_config(config)  # Save default config if not exists

    log_message("=" * 60)
    log_message("Twitter Watcher Started")
    log_message(f"Check Interval: {config['check_interval']} seconds")
    log_message("=" * 60)

    # Get user ID
    user_id, username = get_user_id()
    if not user_id:
        log_message("Failed to authenticate with Twitter API", "ERROR")
        return

    check_count = 0
    since_id = None

    while True:
        check_count += 1
        log_message(f"\n[Check #{check_count}] Starting Twitter check...")

        try:
            # Process mentions
            mention_count, new_since_id = process_mentions(config, user_id, since_id)
            if new_since_id:
                since_id = new_since_id
            log_message(f"✓ Processed {mention_count} mention(s)")

            # Process keyword tracking
            keyword_count = process_keyword_tracking(config)
            log_message(f"✓ Processed {keyword_count} keyword match(es)")

            # Generate summary
            if check_count % 10 == 0:  # Every 10 checks
                generate_summary()

            log_message(f"[Check #{check_count}] Complete - Total: {mention_count + keyword_count} interactions")

        except Exception as e:
            log_message(f"Error during check: {e}", "ERROR")

        if once:
            log_message("\n✓ Single check complete. Exiting.")
            break

        log_message(f"\nWaiting {config['check_interval']} seconds until next check...")
        time.sleep(config['check_interval'])

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Twitter Watcher for AI Employee")
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    args = parser.parse_args()

    if not BEARER_TOKEN:
        log_message("ERROR: Twitter Bearer Token not found in .env file", "ERROR")
        sys.exit(1)

    try:
        watch_twitter(once=args.once)
    except KeyboardInterrupt:
        log_message("\n\n✓ Twitter Watcher stopped by user")
        sys.exit(0)
