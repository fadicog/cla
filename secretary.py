#!/usr/bin/env python3
"""
Secretary Agent - Daily Task Manager
Manages your daily tasks and todo list in a Markdown file.
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


class SecretaryAgent:
    """Secretary agent to manage daily tasks and todo lists."""

    def __init__(self, tasks_file="tasks.md"):
        self.tasks_file = Path(tasks_file)
        self.initialize_tasks_file()

    def initialize_tasks_file(self):
        """Create tasks.md file if it doesn't exist."""
        if not self.tasks_file.exists():
            initial_content = f"""# My Daily Tasks

> Managed by Secretary Agent
> Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Today's Tasks

- [ ] Welcome! Your tasks will appear here.

---

## Completed Tasks

_(Completed tasks will be moved here)_

---

## Notes

Add any important notes or reminders here.
"""
            self.tasks_file.write_text(initial_content, encoding='utf-8')
            print(f"✓ Initialized tasks file: {self.tasks_file}")

    def read_tasks(self):
        """Read all tasks from the MD file."""
        if self.tasks_file.exists():
            return self.tasks_file.read_text(encoding='utf-8')
        return ""

    def add_task(self, task_description, priority="normal"):
        """Add a new task to the todo list."""
        content = self.read_tasks()

        # Create task with priority indicator
        priority_emoji = {"high": "🔴", "normal": "⚪", "low": "🔵"}.get(priority, "⚪")
        new_task = f"- [ ] {priority_emoji} {task_description}"

        # Find the "Today's Tasks" section and add the task
        if "## Today's Tasks" in content:
            parts = content.split("## Today's Tasks")
            if len(parts) > 1:
                section_parts = parts[1].split("---", 1)
                tasks_section = section_parts[0]
                rest = "---" + section_parts[1] if len(section_parts) > 1 else ""

                # Add new task after existing tasks
                tasks_section = tasks_section.rstrip() + f"\n{new_task}\n"

                content = parts[0] + "## Today's Tasks" + tasks_section + rest
        else:
            # Fallback: append to end
            content += f"\n{new_task}\n"

        self.tasks_file.write_text(content, encoding='utf-8')
        print(f"✓ Added task: {task_description}")

    def list_tasks(self):
        """Display all current tasks."""
        content = self.read_tasks()

        print("\n" + "="*60)
        print("📋 YOUR TASKS")
        print("="*60 + "\n")

        # Extract today's tasks
        if "## Today's Tasks" in content:
            parts = content.split("## Today's Tasks")[1].split("---")[0]
            lines = [line.strip() for line in parts.split('\n') if line.strip() and line.strip().startswith('- [')]

            if lines:
                for i, line in enumerate(lines, 1):
                    status = "✓" if "[x]" in line.lower() or "[X]" in line else " "
                    task = line.replace("- [ ]", "").replace("- [x]", "").replace("- [X]", "").strip()
                    print(f"  {i}. [{status}] {task}")
            else:
                print("  No tasks yet. Add one with: python secretary.py add \"Your task\"")
        else:
            print("  No tasks found.")

        print("\n" + "="*60 + "\n")

    def complete_task(self, task_number):
        """Mark a task as completed."""
        content = self.read_tasks()

        if "## Today's Tasks" in content:
            parts = content.split("## Today's Tasks")
            section_parts = parts[1].split("---", 1)
            tasks_section = section_parts[0]
            rest = "---" + section_parts[1] if len(section_parts) > 1 else ""

            lines = tasks_section.split('\n')
            task_lines = [line for line in lines if line.strip().startswith('- [')]

            if 0 < task_number <= len(task_lines):
                # Mark as complete
                old_task = task_lines[task_number - 1]
                completed_task = old_task.replace("- [ ]", "- [x]")

                # Replace in content
                new_tasks_section = tasks_section.replace(old_task, completed_task)
                content = parts[0] + "## Today's Tasks" + new_tasks_section + rest

                # Move to completed section
                if "## Completed Tasks" in content:
                    timestamp = datetime.now().strftime('%Y-%m-%d')
                    completed_entry = f"{completed_task} _(completed {timestamp})_"
                    content = content.replace("## Completed Tasks", f"## Completed Tasks\n\n{completed_entry}")
                    # Remove from today's tasks
                    content = content.replace(completed_task, "", 1)

                self.tasks_file.write_text(content, encoding='utf-8')
                print(f"✓ Completed task #{task_number}")
            else:
                print(f"✗ Invalid task number: {task_number}")

    def remove_task(self, task_number):
        """Remove a task from the list."""
        content = self.read_tasks()

        if "## Today's Tasks" in content:
            parts = content.split("## Today's Tasks")
            section_parts = parts[1].split("---", 1)
            tasks_section = section_parts[0]
            rest = "---" + section_parts[1] if len(section_parts) > 1 else ""

            lines = tasks_section.split('\n')
            task_lines = [line for line in lines if line.strip().startswith('- [')]

            if 0 < task_number <= len(task_lines):
                # Remove the task
                task_to_remove = task_lines[task_number - 1]
                new_tasks_section = tasks_section.replace(task_to_remove + '\n', '', 1)
                content = parts[0] + "## Today's Tasks" + new_tasks_section + rest

                self.tasks_file.write_text(content, encoding='utf-8')
                print(f"✓ Removed task #{task_number}")
            else:
                print(f"✗ Invalid task number: {task_number}")

    def show_help(self):
        """Display help information."""
        help_text = """
Secretary Agent - Your Personal Task Manager

USAGE:
    python secretary.py <command> [arguments]

COMMANDS:
    add <task> [priority]     Add a new task (priority: high, normal, low)
    list                      Show all tasks
    complete <number>         Mark task as completed
    remove <number>           Remove a task
    help                      Show this help message

EXAMPLES:
    python secretary.py add "Buy groceries"
    python secretary.py add "Important meeting" high
    python secretary.py list
    python secretary.py complete 1
    python secretary.py remove 2

PRIORITY LEVELS:
    🔴 high      - Urgent/important tasks
    ⚪ normal    - Regular tasks (default)
    🔵 low       - Low priority tasks

Your tasks are stored in: tasks.md
"""
        print(help_text)


def main():
    """Main entry point for the secretary agent."""
    agent = SecretaryAgent()

    if len(sys.argv) < 2:
        agent.list_tasks()
        print("💡 Tip: Use 'python secretary.py help' for available commands\n")
        return

    command = sys.argv[1].lower()

    if command == "add":
        if len(sys.argv) < 3:
            print("✗ Please provide a task description")
            print("  Usage: python secretary.py add \"Your task description\" [priority]")
            return

        task = sys.argv[2]
        priority = sys.argv[3].lower() if len(sys.argv) > 3 else "normal"
        agent.add_task(task, priority)

    elif command == "list":
        agent.list_tasks()

    elif command == "complete":
        if len(sys.argv) < 3:
            print("✗ Please provide a task number")
            print("  Usage: python secretary.py complete <number>")
            return

        try:
            task_num = int(sys.argv[2])
            agent.complete_task(task_num)
        except ValueError:
            print("✗ Task number must be an integer")

    elif command == "remove":
        if len(sys.argv) < 3:
            print("✗ Please provide a task number")
            print("  Usage: python secretary.py remove <number>")
            return

        try:
            task_num = int(sys.argv[2])
            agent.remove_task(task_num)
        except ValueError:
            print("✗ Task number must be an integer")

    elif command == "help":
        agent.show_help()

    else:
        print(f"✗ Unknown command: {command}")
        print("  Use 'python secretary.py help' for available commands")


if __name__ == "__main__":
    main()
