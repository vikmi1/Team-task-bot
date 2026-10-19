**English** · [Deutsch](README.de.md) · [Русский](README.ru.md)

# Team Task Bot 🤖

A Telegram bot for teamwork — a shared task list with categories and statuses.

The bot's interface is in Russian; the messages below are translated for readability.

## Features

| Command / Button | Description |
|---|---|
| `/start` | Start the bot and show the menu |
| `/add` or `➕ Add task` | Add a task step by step: text → category |
| `/list` or `📋 Task list` | All tasks with buttons to change the status |
| `📂 By category` | Tasks grouped by category |
| `/list_csv` or `📥 Download CSV` | Export all tasks to a `.csv` file |

## Categories

🔧 Development · 🎨 Design · 📢 Marketing · 🧪 Testing · 📋 General

## Statuses

🟡 New → 🔵 In progress → ✅ Done · ❌ Cancelled

## Stack

- **Python 3.10+**
- **aiogram 3** — framework for Telegram bots
- **SQLite3** — local database (built into Python)
- **FSM** (Finite State Machine) — step-by-step data input

## Project structure

```
├── main.py              # Entry point
├── requirements.txt
├── .env.example         # Example config
│
├── db/
│   └── database.py      # SQLite access: init, add, get, update
│
├── handlers/
│   ├── start.py         # /start
│   ├── tasks.py         # /add, /list, /list_csv, callback handlers
│   └── states.py        # FSM states for step-by-step input
│
└── keyboards/
    ├── reply.py         # Persistent menu below the input field
    └── inline.py        # Category and status buttons inside messages
```

## Database schema

```sql
CREATE TABLE tasks (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    text       TEXT    NOT NULL,
    user       TEXT    NOT NULL,
    created_at TEXT    NOT NULL,
    category   TEXT    NOT NULL DEFAULT 'Общее',
    status     TEXT    NOT NULL DEFAULT 'Новая'
);
```

## Installation and running

```bash
# 1. Clone the repository
git clone https://github.com/vikmi1/Team-task-bot.git
cd Team-task-bot

# 2. Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create a .env file with the bot token
cp .env.example .env
# Open .env and paste the token from @BotFather

# 5. Run
python main.py
```

## How to get a token

1. Open [@BotFather](https://t.me/BotFather) in Telegram
2. Send `/newbot`
3. Follow the instructions — you will get a token like `1234567890:AAF...`
4. Put the token into `.env`:
   ```
   BOT_TOKEN=1234567890:AAF...
   ```

## Usage scenario

```
User: /add
Bot:  ✏️ Enter the task text:

User: Prepare the May report
Bot:  📂 Choose a category:
      [🔧 Development] [🎨 Design]
      [📢 Marketing]   [🧪 Testing]
      [📋 General]

User: taps "📢 Marketing"
Bot:  ✅ Task #1 added!
      📝 Prepare the May report
      📢 Category: Marketing
      🟡 Status: New

User: /list
Bot:  📋 All tasks:
      🟡 #1 📢 Marketing
         Prepare the May report
         👤 Ivan · 2026-05-20 23:00
      [✏️ #1]   ← tap to change the status

User: taps "✏️ #1"
Bot:  Choose a new status:
      [🟡 New] [🔵 In progress]
      [✅ Done] [❌ Cancelled]
```
