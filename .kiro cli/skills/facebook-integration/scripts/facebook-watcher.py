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

# Facebook API Configuration
ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")  # Same token works for Facebook
PAGE_ID = os.getenv("FACEBOOK_PAGE_ID", "")
API_VERSION = "v21.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

# Paths
SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "facebook-config.json"
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
        "priority_keywords": ["urgent", "asap", "important", "help"],
        "categories": {
            "customer_inquiry": ["price", "cost", "buy", "purchase", "order"],
            "support": ["help", "issue", "problem", "not working", "error"],
            "feedback": ["love", "great", "amazing", "terrible", "bad"],
            "lead": ["interested", "more info", "contact", "quote"]
        },
        "monitor_comments": True,
        "monitor_messages": True,
        "monitor_mentions": True
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

    log_file = LOGS_DIR / f"facebook-watcher-{datetime.now().strftime('%Y-%m-%d')}.log"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry + "\n")

def make_api_request(endpoint, params=None, method='GET'):
    """Make request to Facebook Graph API"""
    if params is None:
        params = {}
    params['access_token'] = ACCESS_TOKEN

    try:
        if method == 'GET':
            response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
        else:
            response = requests.post(f"{BASE_URL}/{endpoint}", data=params)

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        log_message(f"API request failed: {e}", "ERROR")
        return None

def get_page_id():
    """Get Facebook Page ID from access token"""
    global PAGE_ID
    if PAGE_ID:
        return PAGE_ID

    data = make_api_request("me/accounts")
    if data and 'data' in data and len(data['data']) > 0:
        PAGE_ID = data['data'][0]['id']
        log_message(f"Using Page ID: {PAGE_ID}")
        return PAGE_ID

    log_message("No Facebook Page found", "ERROR")
    return None

def get_page_posts(limit=10):
    """Fetch recent posts from Facebook Page"""
    page_id = get_page_id()
    if not page_id:
        return []

    endpoint = f"{page_id}/posts"
    params = {
        "fields": "id,message,created_time,permalink_url,comments{id,message,from,created_time},reactions.summary(true)",
        "limit": limit
    }

    data = make_api_request(endpoint, params)
    if data and 'data' in data:
        return data['data']
    return []

def get_page_comments():
    """Fetch recent comments on page posts"""
    posts = get_page_posts(5)
    all_comments = []

    for post in posts:
        if 'comments' in post and 'data' in post['comments']:
            for comment in post['comments']['data']:
                comment['post_id'] = post['id']
                comment['post_message'] = post.get('message', '')
                comment['post_url'] = post.get('permalink_url', '')
                all_comments.append(comment)

    return all_comments

def get_page_messages():
    """Fetch messages sent to the Facebook Page"""
    page_id = get_page_id()
    if not page_id:
        return []

    endpoint = f"{page_id}/conversations"
    params = {
        "fields": "id,updated_time,message_count,unread_count,participants,messages{id,created_time,from,to,message}"
    }

    data = make_api_request(endpoint, params)
    if data and 'data' in data:
        return data['data']
    return []

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

def create_action_file(item_type, content, metadata):
    """Create action file in Vault/Needs_Action/"""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    from_user = metadata.get('from', 'unknown').replace(' ', '_')
    filename = f"FACEBOOK_{item_type}_{from_user}_{timestamp}.md"
    filepath = NEEDS_ACTION_DIR / filename

    categories = ", ".join(metadata.get('categories', ['general']))
    priority = metadata.get('priority', 'NORMAL')

    action_content = f"""# FACEBOOK {item_type.upper()}: {metadata.get('subject', 'New Interaction')}

**From:** {metadata.get('from', 'Unknown')}
**Type:** {item_type}
**Category:** {categories}
**Priority:** {priority}
**Timestamp:** {metadata.get('timestamp', datetime.now().isoformat())}
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
*Generated by Facebook Watcher - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(action_content)

    log_message(f"✓ Created action file: {filename}")
    return filepath

def process_comments(config):
    """Process Facebook comments"""
    if not config.get('monitor_comments', True):
        return 0

    log_message("Fetching Facebook comments...")
    comments = get_page_comments()

    processed_count = 0
    for comment in comments:
        comment_text = comment.get('message', '')
        if not comment_text:
            continue

        from_user = comment.get('from', {}).get('name', 'Unknown')
        categories = categorize_content(comment_text, config)
        priority = detect_priority(comment_text, config)

        metadata = {
            'from': from_user,
            'comment_id': comment.get('id'),
            'post_id': comment.get('post_id'),
            'post_message': comment.get('post_message', ''),
            'timestamp': comment.get('created_time'),
            'categories': categories,
            'priority': priority,
            'subject': f"Comment from {from_user}",
            'url': comment.get('post_url', 'N/A')
        }

        create_action_file("COMMENT", comment_text, metadata)
        processed_count += 1

    return processed_count

def process_messages(config):
    """Process Facebook messages"""
    if not config.get('monitor_messages', True):
        return 0

    log_message("Fetching Facebook messages...")
    conversations = get_page_messages()

    processed_count = 0
    for conversation in conversations:
        if conversation.get('unread_count', 0) > 0:
            messages = conversation.get('messages', {}).get('data', [])
            for message in messages:
                msg_text = message.get('message', '')
                if not msg_text:
                    continue

                from_user = message.get('from', {}).get('name', 'Unknown')
                categories = categorize_content(msg_text, config)
                priority = detect_priority(msg_text, config)

                metadata = {
                    'from': from_user,
                    'conversation_id': conversation.get('id'),
                    'message_id': message.get('id'),
                    'timestamp': message.get('created_time'),
                    'categories': categories,
                    'priority': priority,
                    'subject': f"Message from {from_user}",
                    'url': f"https://www.facebook.com/messages/"
                }

                create_action_file("MESSAGE", msg_text, metadata)
                processed_count += 1

    return processed_count

def generate_summary():
    """Generate daily summary of Facebook activity"""
    log_message("Generating Facebook activity summary...")

    # Count action files
    action_files = list(NEEDS_ACTION_DIR.glob("FACEBOOK_*.md"))
    done_files = list(DONE_DIR.glob("FACEBOOK_*.md"))

    summary = f"""# Facebook Activity Summary
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Statistics
- Pending Actions: {len(action_files)}
- Completed Actions: {len(done_files)}
- Total Interactions: {len(action_files) + len(done_files)}

## Pending Actions
"""

    for action_file in action_files[:10]:  # Show first 10
        summary += f"- {action_file.name}\n"

    summary_file = LOGS_DIR / f"facebook-summary-{datetime.now().strftime('%Y-%m-%d')}.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary)

    log_message(f"✓ Summary saved: {summary_file.name}")
    return summary_file

def watch_facebook(once=False):
    """Main watcher loop"""
    config = load_config()
    save_config(config)  # Save default config if not exists

    log_message("=" * 60)
    log_message("Facebook Watcher Started")
    log_message(f"Check Interval: {config['check_interval']} seconds")
    log_message("=" * 60)

    check_count = 0

    while True:
        check_count += 1
        log_message(f"\n[Check #{check_count}] Starting Facebook check...")

        try:
            # Process comments
            comment_count = process_comments(config)
            log_message(f"✓ Processed {comment_count} comment(s)")

            # Process messages
            msg_count = process_messages(config)
            log_message(f"✓ Processed {msg_count} message(s)")

            # Generate summary
            if check_count % 10 == 0:  # Every 10 checks
                generate_summary()

            log_message(f"[Check #{check_count}] Complete - Total: {comment_count + msg_count} interactions")

        except Exception as e:
            log_message(f"Error during check: {e}", "ERROR")

        if once:
            log_message("\n✓ Single check complete. Exiting.")
            break

        log_message(f"\nWaiting {config['check_interval']} seconds until next check...")
        time.sleep(config['check_interval'])

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Facebook Watcher for AI Employee")
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    args = parser.parse_args()

    if not ACCESS_TOKEN:
        log_message("ERROR: Facebook access token not found in .env file", "ERROR")
        sys.exit(1)

    try:
        watch_facebook(once=args.once)
    except KeyboardInterrupt:
        log_message("\n\n✓ Facebook Watcher stopped by user")
        sys.exit(0)
