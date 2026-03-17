#!/usr/bin/env python3
"""
Approval Workflow Manager
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ApprovalWorkflow')

class ApprovalManager:
    def __init__(self, vault_path='../../Vault'):
        self.vault_path = Path(vault_path)
        self.pending_path = self.vault_path / 'Pending_Approval'
        self.done_path = self.vault_path / 'Done'

        # Ensure directories exist
        self.pending_path.mkdir(parents=True, exist_ok=True)
        self.done_path.mkdir(parents=True, exist_ok=True)

    def create_approval_request(self, action_type: str, details: Dict) -> Path:
        """Create approval request file"""
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f"APPROVAL_{action_type}_{timestamp}.md"
        filepath = self.pending_path / filename

        content = self.format_approval_request(action_type, details)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"Approval request created: {filename}")
        return filepath

    def format_approval_request(self, action_type: str, details: Dict) -> str:
        """Format approval request content"""
        content = f"""# APPROVAL REQUEST: {details.get('title', action_type)}

**Type:** {action_type}
**Priority:** {details.get('priority', 'MEDIUM')}
**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Requires Approval By:** {details.get('deadline', 'ASAP')}

## Action Details

"""

        # Add action-specific details
        for key, value in details.items():
            if key not in ['title', 'priority', 'deadline', 'risk_assessment']:
                content += f"**{key.replace('_', ' ').title()}:** {value}\n"

        content += "\n## Risk Assessment\n\n"

        risk = details.get('risk_assessment', {})
        for key, value in risk.items():
            content += f"- **{key.replace('_', ' ').title()}:** {value}\n"

        content += """

## Approval Decision

**Status:** PENDING

[ ] APPROVE - Execute as planned
[ ] APPROVE WITH CHANGES - Modify before executing
[ ] REJECT - Do not execute

**Approved By:** _____________
**Date:** _____________
**Notes:** _____________

---

*To approve: Change status to APPROVED and add your name*
*To reject: Change status to REJECTED and add reason*
"""

        return content

    def list_pending_approvals(self) -> List[Dict]:
        """List all pending approval requests"""
        approvals = []

        for file_path in self.pending_path.glob('APPROVAL_*.md'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                status = self.parse_approval_status(content)

                approvals.append({
                    'filename': file_path.name,
                    'filepath': str(file_path),
                    'status': status,
                    'created': file_path.stat().st_mtime
                })
            except Exception as e:
                logger.error(f"Error reading {file_path.name}: {e}")

        return approvals

    def parse_approval_status(self, content: str) -> str:
        """Parse approval status from content"""
        if 'Status:** APPROVED' in content or '[X] APPROVE' in content:
            return 'APPROVED'
        elif 'Status:** REJECTED' in content or '[X] REJECT' in content:
            return 'REJECTED'
        else:
            return 'PENDING'

    def check_approval(self, filepath: str) -> Dict:
        """Check approval status of a specific file"""
        file_path = Path(filepath)

        if not file_path.exists():
            return {'status': 'NOT_FOUND', 'message': 'File not found'}

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        status = self.parse_approval_status(content)

        return {
            'status': status,
            'filepath': str(file_path),
            'content': content
        }

    def approve_action(self, filepath: str, approver: str, notes: str = '') -> bool:
        """Approve an action"""
        file_path = Path(filepath)

        if not file_path.exists():
            logger.error(f"File not found: {filepath}")
            return False

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update approval status
        content = content.replace('**Status:** PENDING', '**Status:** APPROVED')
        content = content.replace('[ ] APPROVE', '[X] APPROVE')
        content = content.replace('**Approved By:** _____________', f'**Approved By:** {approver}')
        content = content.replace('**Date:** _____________', f'**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

        if notes:
            content = content.replace('**Notes:** _____________', f'**Notes:** {notes}')

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"✓ Approved: {file_path.name}")
        return True

    def reject_action(self, filepath: str, approver: str, reason: str) -> bool:
        """Reject an action"""
        file_path = Path(filepath)

        if not file_path.exists():
            logger.error(f"File not found: {filepath}")
            return False

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update approval status
        content = content.replace('**Status:** PENDING', '**Status:** REJECTED')
        content = content.replace('[ ] REJECT', '[X] REJECT')
        content = content.replace('**Approved By:** _____________', f'**Rejected By:** {approver}')
        content = content.replace('**Date:** _____________', f'**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        content = content.replace('**Notes:** _____________', f'**Notes:** {reason}')

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"✗ Rejected: {file_path.name}")
        return True

    def move_to_done(self, filepath: str):
        """Move approved/rejected file to Done folder"""
        file_path = Path(filepath)
        dest_path = self.done_path / file_path.name

        file_path.rename(dest_path)
        logger.info(f"Moved to Done: {file_path.name}")

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Approval Workflow Manager')
    parser.add_argument('--vault-path', default='../../Vault', help='Path to vault')
    parser.add_argument('--list', action='store_true', help='List pending approvals')
    parser.add_argument('--check', help='Check specific approval file')
    parser.add_argument('--approve', help='Approve specific file')
    parser.add_argument('--reject', help='Reject specific file')
    parser.add_argument('--approver', default='User', help='Approver name')
    parser.add_argument('--reason', help='Rejection reason')
    parser.add_argument('--notes', help='Approval notes')

    args = parser.parse_args()

    manager = ApprovalManager(vault_path=args.vault_path)

    if args.list:
        approvals = manager.list_pending_approvals()
        print(f"\nPending Approvals: {len(approvals)}\n")
        for approval in approvals:
            print(f"- {approval['filename']} [{approval['status']}]")

    elif args.check:
        result = manager.check_approval(args.check)
        print(f"\nStatus: {result['status']}")

    elif args.approve:
        manager.approve_action(args.approve, args.approver, args.notes or '')

    elif args.reject:
        if not args.reason:
            print("Error: --reason required for rejection")
        else:
            manager.reject_action(args.reject, args.approver, args.reason)

if __name__ == '__main__':
    main()
