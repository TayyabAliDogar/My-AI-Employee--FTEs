#!/usr/bin/env python3
"""
Plan Creator - Generates execution plans for Claude Code
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('PlanCreator')

class PlanCreator:
    def __init__(self, vault_path='../../Vault', config_path='plan-config.json'):
        self.vault_path = Path(vault_path)
        self.needs_action_path = self.vault_path / 'Needs_Action'
        self.config = self.load_config(config_path)

    def load_config(self, config_path):
        """Load configuration"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                'max_tasks_per_plan': 10,
                'priority_rules': {
                    'urgent_keywords': ['urgent', 'asap', 'critical', 'emergency'],
                    'high_value_threshold': 1000,
                    'client_priority': True
                },
                'approval_rules': {
                    'financial_threshold': 500,
                    'external_communication': True,
                    'legal_documents': True
                }
            }

    def scan_tasks(self) -> List[Dict]:
        """Scan Needs_Action folder for tasks"""
        tasks = []

        if not self.needs_action_path.exists():
            logger.warning(f"Needs_Action folder not found: {self.needs_action_path}")
            return tasks

        for file_path in self.needs_action_path.glob('*.md'):
            if file_path.name == 'PLAN.md':
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                task = {
                    'filename': file_path.name,
                    'filepath': str(file_path),
                    'content': content,
                    'type': self.detect_task_type(file_path.name),
                    'priority': self.calculate_priority(content, file_path.name),
                    'requires_approval': self.requires_approval(content, file_path.name)
                }

                tasks.append(task)

            except Exception as e:
                logger.error(f"Error reading {file_path.name}: {e}")

        return tasks

    def detect_task_type(self, filename: str) -> str:
        """Detect task type from filename"""
        if filename.startswith('EMAIL_'):
            return 'email'
        elif filename.startswith('WHATSAPP_'):
            return 'whatsapp'
        elif filename.startswith('DOCUMENT_'):
            return 'document'
        elif filename.startswith('ACTION_'):
            return 'action'
        else:
            return 'general'

    def calculate_priority(self, content: str, filename: str) -> str:
        """Calculate task priority"""
        content_lower = content.lower()
        filename_lower = filename.lower()

        urgent_keywords = self.config['priority_rules']['urgent_keywords']

        # Check for urgent keywords
        if any(keyword in content_lower or keyword in filename_lower for keyword in urgent_keywords):
            return 'HIGH'

        # Check for client-related content
        if self.config['priority_rules']['client_priority']:
            if 'client' in content_lower or 'customer' in content_lower:
                return 'HIGH'

        # Check for financial content
        if 'invoice' in content_lower or 'payment' in content_lower or '$' in content:
            return 'HIGH'

        # Default to medium
        return 'MEDIUM'

    def requires_approval(self, content: str, filename: str) -> bool:
        """Check if task requires human approval"""
        content_lower = content.lower()

        # External communication
        if self.config['approval_rules']['external_communication']:
            if 'send email' in content_lower or 'post' in content_lower:
                return True

        # Financial transactions
        if self.config['approval_rules']['financial_threshold']:
            if 'payment' in content_lower or 'invoice' in content_lower:
                return True

        # Legal documents
        if self.config['approval_rules']['legal_documents']:
            if 'contract' in content_lower or 'agreement' in content_lower:
                return True

        return False

    def sort_tasks(self, tasks: List[Dict]) -> Dict[str, List[Dict]]:
        """Sort tasks by priority"""
        sorted_tasks = {
            'HIGH': [],
            'MEDIUM': [],
            'LOW': []
        }

        for task in tasks:
            priority = task['priority']
            sorted_tasks[priority].append(task)

        return sorted_tasks

    def generate_plan(self, tasks: List[Dict]) -> str:
        """Generate execution plan"""
        if not tasks:
            return None

        sorted_tasks = self.sort_tasks(tasks)
        total_tasks = len(tasks)
        estimated_time = total_tasks * 3  # 3 minutes per task estimate

        plan = f"""# EXECUTION PLAN

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Tasks:** {total_tasks}
**Estimated Time:** {estimated_time} minutes

## Priority Queue

"""

        # Add HIGH priority tasks
        if sorted_tasks['HIGH']:
            plan += "### HIGH PRIORITY (Execute First)\n\n"
            for i, task in enumerate(sorted_tasks['HIGH'], 1):
                plan += f"{i}. {task['filename']}\n"
            plan += "\n"

        # Add MEDIUM priority tasks
        if sorted_tasks['MEDIUM']:
            plan += "### MEDIUM PRIORITY\n\n"
            for i, task in enumerate(sorted_tasks['MEDIUM'], len(sorted_tasks['HIGH']) + 1):
                plan += f"{i}. {task['filename']}\n"
            plan += "\n"

        # Add LOW priority tasks
        if sorted_tasks['LOW']:
            plan += "### LOW PRIORITY (If Time Permits)\n\n"
            for i, task in enumerate(sorted_tasks['LOW'], len(sorted_tasks['HIGH']) + len(sorted_tasks['MEDIUM']) + 1):
                plan += f"{i}. {task['filename']}\n"
            plan += "\n"

        plan += "## Execution Strategy\n\n"

        # Add detailed task instructions
        task_num = 1
        for priority in ['HIGH', 'MEDIUM', 'LOW']:
            for task in sorted_tasks[priority]:
                plan += f"### Task {task_num}: {task['filename']} ({priority})\n\n"
                plan += f"- **File:** {task['filename']}\n"
                plan += f"- **Type:** {task['type']}\n"
                plan += f"- **Action:** Read and analyze content, take appropriate action\n"

                if task['requires_approval']:
                    plan += f"- **Approval:** Required before execution\n"
                else:
                    plan += f"- **Approval:** Not required\n"

                plan += f"- **Estimated Time:** 3 minutes\n\n"
                task_num += 1

        # Add approval requirements section
        approval_tasks = [t for t in tasks if t['requires_approval']]
        if approval_tasks:
            plan += "## Approval Requirements\n\n"
            for task in approval_tasks:
                plan += f"- {task['filename']}: Human approval required\n"
            plan += "\n"

        plan += """## Success Criteria

- All HIGH priority tasks completed
- Approval requests created for sensitive actions
- All outputs saved to appropriate folders
- Dashboard updated with results

---

*Auto-generated by Plan Creator*
"""

        return plan

    def save_plan(self, plan: str):
        """Save plan to Needs_Action folder"""
        plan_path = self.needs_action_path / 'PLAN.md'

        with open(plan_path, 'w', encoding='utf-8') as f:
            f.write(plan)

        logger.info(f"Plan saved to: {plan_path}")
        return plan_path

    def create_plan(self):
        """Main plan creation workflow"""
        logger.info("Scanning for tasks...")
        tasks = self.scan_tasks()

        if not tasks:
            logger.info("No tasks found in Needs_Action folder")
            return None

        logger.info(f"Found {len(tasks)} task(s)")

        # Limit tasks per plan
        max_tasks = self.config['max_tasks_per_plan']
        if len(tasks) > max_tasks:
            logger.warning(f"Too many tasks ({len(tasks)}), limiting to {max_tasks}")
            tasks = tasks[:max_tasks]

        logger.info("Generating execution plan...")
        plan = self.generate_plan(tasks)

        if plan:
            plan_path = self.save_plan(plan)
            logger.info(f"✓ Plan created successfully: {plan_path}")
            return plan_path
        else:
            logger.error("Failed to generate plan")
            return None

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Create execution plan for Claude Code')
    parser.add_argument('--vault-path', default='../../Vault', help='Path to Obsidian vault')
    parser.add_argument('--dry-run', action='store_true', help='Preview plan without saving')
    parser.add_argument('--focus', help='Focus on specific priority (HIGH, MEDIUM, LOW)')

    args = parser.parse_args()

    creator = PlanCreator(vault_path=args.vault_path)

    if args.dry_run:
        tasks = creator.scan_tasks()
        if tasks:
            plan = creator.generate_plan(tasks)
            print(plan)
        else:
            print("No tasks found")
    else:
        creator.create_plan()

if __name__ == '__main__':
    main()
