# Agentic AI-Based Personalized Assistant for Important Emails, Task Display, and Automated Reminders

## Project Overview
This project is a **final-year level** Python assistant that:
- Detects **important emails** (sender, keywords, unread status).
- Manages **tasks** with a SQLite database.
- Runs **automated reminders** every minute.
- Uses a **lightweight agent** to understand user intent and trigger tools.

The design is intentionally simple and modular for easy understanding in a viva.

**Note:** This is a **console-based (CLI) application**, not a web app. It runs locally in your terminal.

## Architecture
```
AI_Assistant/
├── main.py            # Entry point and CLI
├── email_agent.py     # Email fetching + important detection
├── task_manager.py    # Task CRUD with SQLite
├── reminder_agent.py  # Background scheduler and reminders
├── agent_controller.py# Rule-based agentic controller
├── database.py        # SQLite connection + schema
├── display.py         # Output formatting
├── config.py          # Config and keywords
├── requirements.txt   # Dependencies
└── README.md          # Documentation
```

## How the Agent Works
The `AgentController` performs lightweight planning:
1. **Detect intent** using simple keyword rules (e.g., "check email").
2. **Plan actions** (select tool: email checker, task manager, reminders).
3. **Execute** tools and show results.

This avoids heavy frameworks while still demonstrating agentic behavior.

## Email Notes
By default, the project uses **dummy emails** for a smooth demo. To use IMAP:
- Update `config.py` with real credentials and set `use_dummy_emails = False`.
- Use an app password if using Gmail.

## How to Run (Local CLI)
1. Open a terminal and move into the project folder:
   ```bash
   cd AI_Assistant
   ```
2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   ```
   - Windows:
     ```bash
     .venv\\Scripts\\activate
     ```
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the assistant:
   ```bash
   python main.py
   ```

### Example Commands
```
check email
add task title=ProjectDemo date=2025-01-10 time=14:00 priority=High
show tasks
start reminders
```

## Sample Data
Dummy emails include exam deadlines and interview messages to showcase important email detection.
