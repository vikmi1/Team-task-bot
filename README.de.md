[English](README.md) · **Deutsch** · [Русский](README.ru.md)

# Team Task Bot 🤖

Ein Telegram-Bot für die Teamarbeit – eine gemeinsame Aufgabenliste mit Kategorien und Status.

Die Oberfläche des Bots ist auf Russisch; die Nachrichten unten sind zur besseren Lesbarkeit übersetzt.

## Funktionen

| Befehl / Schaltfläche | Beschreibung |
|---|---|
| `/start` | Bot starten, Menü anzeigen |
| `/add` oder `➕ Aufgabe hinzufügen` | Aufgabe schrittweise anlegen: Text → Kategorie |
| `/list` oder `📋 Aufgabenliste` | Alle Aufgaben mit Schaltflächen zum Statuswechsel |
| `📂 Nach Kategorien` | Aufgaben nach Kategorie gruppiert |
| `/list_csv` oder `📥 CSV herunterladen` | Export aller Aufgaben in eine `.csv`-Datei |

## Kategorien

🔧 Entwicklung · 🎨 Design · 📢 Marketing · 🧪 Testen · 📋 Allgemein

## Status

🟡 Neu → 🔵 In Arbeit → ✅ Erledigt · ❌ Abgebrochen

## Stack

- **Python 3.10+**
- **aiogram 3** – Framework für Telegram-Bots
- **SQLite3** – lokale Datenbank (in Python integriert)
- **FSM** (Finite State Machine) – schrittweise Dateneingabe

## Projektstruktur

```
├── main.py              # Einstiegspunkt
├── requirements.txt
├── .env.example         # Beispielkonfiguration
│
├── db/
│   └── database.py      # Zugriff auf SQLite: init, add, get, update
│
├── handlers/
│   ├── start.py         # /start
│   ├── tasks.py         # /add, /list, /list_csv, Callback-Handler
│   └── states.py        # FSM-Zustände für die schrittweise Eingabe
│
└── keyboards/
    ├── reply.py         # Dauerhaftes Menü unter dem Eingabefeld
    └── inline.py        # Kategorie- und Status-Schaltflächen in Nachrichten
```

## Datenbankschema

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

## Installation und Start

```bash
# 1. Repository klonen
git clone https://github.com/vikmi1/Team-task-bot.git
cd Team-task-bot

# 2. Virtuelle Umgebung anlegen
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac / Linux

# 3. Abhängigkeiten installieren
pip install -r requirements.txt

# 4. Datei .env mit dem Bot-Token anlegen
cp .env.example .env
# .env öffnen und den Token von @BotFather einfügen

# 5. Starten
python main.py
```

## Token erhalten

1. [@BotFather](https://t.me/BotFather) in Telegram öffnen
2. `/newbot` senden
3. Den Anweisungen folgen – man erhält einen Token der Form `1234567890:AAF...`
4. Token in `.env` eintragen:
   ```
   BOT_TOKEN=1234567890:AAF...
   ```

## Ablaufbeispiel

```
Nutzer: /add
Bot:    ✏️ Text der Aufgabe eingeben:

Nutzer: Bericht für Mai vorbereiten
Bot:    📂 Kategorie wählen:
        [🔧 Entwicklung] [🎨 Design]
        [📢 Marketing]   [🧪 Testen]
        [📋 Allgemein]

Nutzer: tippt auf „📢 Marketing"
Bot:    ✅ Aufgabe #1 hinzugefügt!
        📝 Bericht für Mai vorbereiten
        📢 Kategorie: Marketing
        🟡 Status: Neu

Nutzer: /list
Bot:    📋 Alle Aufgaben:
        🟡 #1 📢 Marketing
           Bericht für Mai vorbereiten
           👤 Ivan · 2026-05-20 23:00
        [✏️ #1]   ← antippen, um den Status zu ändern

Nutzer: tippt auf „✏️ #1"
Bot:    Neuen Status wählen:
        [🟡 Neu] [🔵 In Arbeit]
        [✅ Erledigt] [❌ Abgebrochen]
```
