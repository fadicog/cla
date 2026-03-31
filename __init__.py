"""
Secretary Agent Package
Daily task & schedule management system for product managers and teams.

AGENT SPECIFICATION: See agent_secretary.md for complete role definition,
workflows, templates, and collaboration patterns.

CAPABILITIES:
- Task management with priority levels (High, Medium, Low, Backlog)
- Task status tracking (Pending, In Progress, Completed, Blocked)
- Meeting action items and follow-ups
- Weekly reporting and metrics
- Markdown-based task storage (tasks.md)
- CLI interface for quick task operations

USAGE (Python API):
    from secretary import SecretaryAgent

    agent = SecretaryAgent()
    agent.add_task("Complete project report", priority="high")
    agent.list_tasks()

USAGE (CLI):
    python secretary.py add "Your task description"
    python secretary.py add "Urgent task" high
    python secretary.py list
    python secretary.py complete 1
    python secretary.py help

AGENT COLLABORATION:
- Works with Main PM Agent for stakeholder reporting
- Tracks deliverables from New Feature Agent
- Manages follow-ups from Existing Feature Agent
- Coordinates across all product work streams

DOCUMENTATION:
- Agent Spec: agent_secretary.md
- Task Storage: tasks.md (auto-generated)
- Templates: See agent_secretary.md for full template library

Version: 1.0.0
Created: 2025-11-20
"""

__version__ = "1.0.0"
__author__ = "Secretary Agent"
__all__ = ["SecretaryAgent"]

from secretary import SecretaryAgent
