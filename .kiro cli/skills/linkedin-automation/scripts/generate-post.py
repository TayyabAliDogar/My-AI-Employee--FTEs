#!/usr/bin/env python3
"""
Generate LinkedIn post content based on business context
"""

import os
import json
import random
from datetime import datetime
from pathlib import Path

class LinkedInPostGenerator:
    def __init__(self, vault_path='../../Vault'):
        self.vault_path = Path(vault_path)
        self.templates = self.load_templates()

    def load_templates(self):
        """Load post templates"""
        return {
            'industry_insights': [
                "🚀 {insight}\n\n{body}\n\nKey takeaways:\n{takeaways}\n\nWhat's your experience? 👇\n\n{hashtags}",
                "💡 {insight}\n\n{body}\n\n{cta}\n\n{hashtags}"
            ],
            'company_updates': [
                "📢 Exciting news!\n\n{body}\n\nThis means {benefit}\n\n{cta}\n\n{hashtags}"
            ],
            'tips_and_tricks': [
                "💼 Pro Tip: {tip}\n\n{body}\n\nTry this:\n{steps}\n\n{hashtags}"
            ]
        }

    def analyze_recent_activity(self):
        """Analyze recent business activity from vault"""
        done_path = self.vault_path / 'Done'

        if not done_path.exists():
            return None

        recent_files = sorted(done_path.glob('*.md'), key=lambda x: x.stat().st_mtime, reverse=True)[:5]

        activities = []
        for file in recent_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                activities.append({
                    'filename': file.name,
                    'content': content[:200]
                })

        return activities

    def generate_post(self, theme='industry_insights'):
        """Generate LinkedIn post"""

        # Example post generation
        posts = {
            'industry_insights': {
                'insight': 'The Future of AI in Business Automation',
                'body': 'We\'re seeing a massive shift in how businesses operate. AI isn\'t just a tool anymore—it\'s becoming a full-time employee.\n\nAt our company, we\'ve automated 70% of routine tasks, freeing our team to focus on strategic work.',
                'takeaways': '• AI handles repetitive tasks\n• Teams focus on high-value work\n• Productivity increases 3x',
                'hashtags': '#AI #BusinessAutomation #Productivity #Innovation'
            },
            'company_updates': {
                'body': 'We just completed our 100th automated workflow this month! 🎉\n\nOur AI Employee system is now handling:\n• Email management\n• Client communications\n• Report generation\n• Task scheduling',
                'benefit': 'our team can focus on what matters most—serving our clients better.',
                'cta': 'Want to learn how we did it? Drop a comment below!',
                'hashtags': '#Automation #BusinessGrowth #AI'
            },
            'tips_and_tricks': {
                'tip': 'Automate Your Morning Routine',
                'body': 'Start your day with a clean slate. Here\'s how we use AI to prepare for each day:',
                'steps': '1. AI reviews overnight emails\n2. Prioritizes urgent items\n3. Drafts responses\n4. Creates daily plan\n\nResult? We start each day 2 hours ahead.',
                'hashtags': '#ProductivityHacks #TimeManagement #AI'
            }
        }

        template = random.choice(self.templates.get(theme, self.templates['industry_insights']))
        post_data = posts.get(theme, posts['industry_insights'])

        post = template.format(**post_data)

        return post

    def save_draft(self, post, theme):
        """Save post draft for approval"""
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f"LINKEDIN_DRAFT_{theme}_{timestamp}.md"
        filepath = self.vault_path / 'Pending_Approval' / filename

        content = f"""# LINKEDIN POST DRAFT

**Theme:** {theme}
**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Status:** PENDING APPROVAL

## Post Content

{post}

## Approval

[ ] APPROVE - Post to LinkedIn
[ ] APPROVE WITH CHANGES - Edit before posting
[ ] REJECT - Do not post

**Approved By:** _____________
**Date:** _____________
**Notes:** _____________

---

*To approve: Mark checkbox and add your name*
*To post: Run linkedin-post.py with this content*
"""

        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✓ Draft saved: {filename}")
        return filepath

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Generate LinkedIn post')
    parser.add_argument('--theme', default='industry_insights',
                       choices=['industry_insights', 'company_updates', 'tips_and_tricks'],
                       help='Post theme')
    parser.add_argument('--vault-path', default='../../Vault', help='Path to vault')
    parser.add_argument('--preview', action='store_true', help='Preview without saving')

    args = parser.parse_args()

    generator = LinkedInPostGenerator(vault_path=args.vault_path)
    post = generator.generate_post(theme=args.theme)

    if args.preview:
        print("\n" + "="*60)
        print("PREVIEW")
        print("="*60 + "\n")
        print(post)
        print("\n" + "="*60)
    else:
        filepath = generator.save_draft(post, args.theme)
        print(f"\nDraft saved to: {filepath}")
        print("Review and approve before posting to LinkedIn")

if __name__ == '__main__':
    main()
