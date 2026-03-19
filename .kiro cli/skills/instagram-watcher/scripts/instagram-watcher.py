import os
import sys
import json
import time
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

# Paths
SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "instagram-config.json"
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
            "collaboration": ["collab", "partnership", "sponsor", "work together"]
        }
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

    log_file = LOGS_DIR / f"instagram-watcher-{datetime.now().strftime('%Y-%m-%d')}.log"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry + "\n")

def make_api_request(endpoint, params=None):
    """Make request to Instagram Graph API"""
    if params is None:
        params = {}
    params['access_token'] = ACCESS_TOKEN

    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        log_message(f"API request failed: {e}", "ERROR")
        return None

def get_instagram_messages():
    """Fetch Instagram messages (conversations)"""
    endpoint = f"{ACCOUNT_ID}/conversations"
    params = {
        "fields": "id,updated_time,message_count,unread_count,participants,messages{id,created_time,from,to,message}",
        "platform": "instagram"
    }

    data = make_api_request(endpoint, params)
    if data and 'data' in data:
        return data['data']
    return []

def get_instagram_comments():
    """Fetch recent comments on Instagram posts"""
    # First get recent media
    endpoint = f"{ACCOUNT_ID}/media"
    params = {
        "fields": "id,caption,media_type,timestamp,permalink"
    }

    media_data = make_api_request(endpoint, params)
    if not media_data or 'data' not in media_data:
        return []

    all_comments = []
    for media in media_data['data'][:5]:  # Check last 5 posts
        comment_endpoint = f"{media['id']}/comments"
        comment_params = {
            "fields": "id,text,username,timestamp,from"
        }

        comments_data = make_api_request(comment_endpoint, comment_params)
        if comments_data and 'data' in comments_data:
            for comment in comments_data['data']:
                comment['media_id'] = media['id']
                comment['media_caption'] = media.get('caption', '')
                comment['media_url'] = media.get('permalink', '')
                all_comments.append(comment)

    return all_comments

def categorize_content(text, config):
    """Categorize content based on keywords"""
    text_lower = text.lower()
    categories = []

    for category, keywords in config['categories'].items():
        if any(keyword in text_lower for keyword in keywords):
            categories.append(category)

    return categories if categories else ["general"]

def detect_priority(text, config):
    """Detect if content is high priority"""
    text_lower = text.lower()
    for keyword in config['priority_keywords']:
        if keyword in text_lower:
            return "HIGH"
    return "NORMAL"

def create_action_file(item_type, content, metadata):
    """Create action file in Vault/Needs_Action/"""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"INSTAGRAM_{item_type}_{metadata.get('from', 'unknown')}_{timestamp}.md"
    filepath = NEEDS_ACTION_DIR / filename

    categories = ", ".join(metadata.get('categories', ['general']))
    priority = metadata.get('priority', 'NORMAL')

    action_content = f"""# INSTAGRAM {item_type.upper()}: {metadata.get('subject', 'New Interaction')}

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
*Generated by Instagram Watcher - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(action_content)

    log_message(f"✓ Created action file: {filename}")
    return filepath

def process_messages(config):
    """Process Instagram messages"""
    log_message("Fetching Instagram messages...")
    conversations = get_instagram_messages()

    processed_count = 0
    for conversation in conversations:
        if conversation.get('unread_count', 0) > 0:
            messages = conversation.get('messages', {}).get('data', [])
            for message in messages:
                msg_text = message.get('message', '')
                if not msg_text:
                    continue

                from_user = message.get('from', {}).get('username', 'Unknown')
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
                    'url': f"https://www.instagram.com/direct/inbox/"
                }

                create_action_file("MESSAGE", msg_text, metadata)
                processed_count += 1

    return processed_count

def process_comments(config):
    """Process Instagram comments"""
    log_message("Fetching Instagram comments...")
    comments = get_instagram_comments()

    processed_count = 0
    for comment in comments:
        comment_text = comment.get('text', '')
        if not comment_text:
            continue

        username = comment.get('username', 'Unknown')
        categories = categorize_content(comment_text, config)
        priority = detect_priority(comment_text, config)

        metadata = {
            'from': username,
            'comment_id': comment.get('id'),
            'media_id': comment.get('media_id'),
            'media_caption': comment.get('media_caption', ''),
            'timestamp': comment.get('timestamp'),
            'categories': categories,
            'priority': priority,
            'subject': f"Comment from {username}",
            'url': comment.get('media_url', 'N/A')
        }

        create_action_file("COMMENT", comment_text, metadata)
        processed_count += 1

    return processed_count

def generate_summary():
    """Generate daily summary of Instagram activity"""
    log_message("Generating Instagram activity summary...")

    # Count action files
    action_files = list(NEEDS_ACTION_DIR.glob("INSTAGRAM_*.md"))
    done_files = list(DONE_DIR.glob("INSTAGRAM_*.md"))

    summary = f"""# Instagram Activity Summary
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Statistics
- Pending Actions: {len(action_files)}
- Completed Actions: {len(done_files)}
- Total Interactions: {len(action_files) + len(done_files)}

## Pending Actions
"""

    for action_file in action_files[:10]:  # Show first 10
        summary += f"- {action_file.name}\n"

    summary_file = LOGS_DIR / f"instagram-summary-{datetime.now().strftime('%Y-%m-%d')}.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary)

    log_message(f"✓ Summary saved: {summary_file.name}")
    return summary_file

def watch_instagram(once=False):
    """Main watcher loop"""
    config = load_config()
    save_config(config)  # Save default config if not exists

    log_message("=" * 60)
    log_message("Instagram Watcher Started")
    log_message(f"Account ID: {ACCOUNT_ID}")
    log_message(f"Check Interval: {config['check_interval']} seconds")
    log_message("=" * 60)

    check_count = 0

    while True:
        check_count += 1
        log_message(f"\n[Check #{check_count}] Starting Instagram check...")

        try:
            # Process messages
            msg_count = process_messages(config)
            log_message(f"✓ Processed {msg_count} message(s)")

            # Process comments
            comment_count = process_comments(config)
            log_message(f"✓ Processed {comment_count} comment(s)")

            # Generate summary
            if check_count % 10 == 0:  # Every 10 checks
                generate_summary()

            log_message(f"[Check #{check_count}] Complete - Total: {msg_count + comment_count} interactions")

        except Exception as e:
            log_message(f"Error during check: {e}", "ERROR")

        if once:
            log_message("\n✓ Single check complete. Exiting.")
            break

        log_message(f"\nWaiting {config['check_interval']} seconds until next check...")
        time.sleep(config['check_interval'])

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Instagram Watcher for AI Employee")
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    args = parser.parse_args()

    if not ACCESS_TOKEN or not ACCOUNT_ID:
        log_message("ERROR: Instagram credentials not found in .env file", "ERROR")
        sys.exit(1)

    try:
        watch_instagram(once=args.once)
    except KeyboardInterrupt:
        log_message("\n\n✓ Instagram Watcher stopped by user")
        sys.exit(0)
