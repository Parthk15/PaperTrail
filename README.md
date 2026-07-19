# PaperTrail

**Learn • Organize • Recall**

A lightweight, offline study companion built in Python. Take notes, plan your day, review flashcards, generate quizzes, and summarize text — all from your terminal, with no account or internet connection required.

**Version:** v0.1.0  
**Author:** Parth K

---

## Features

| Module | What it does |
|--------|--------------|
| **Notes** | Create, edit, delete, search, and categorize notes |
| **Flashcards** | Build decks, review cards, and track correct/incorrect stats |
| **Quiz Generator** | Create multiple-choice quizzes manually or auto-generate from notes |
| **AI Summary** | Summarize long text or saved notes using an offline extractive algorithm |
| **Daily Planner** | Add tasks with dates, priorities, and completion tracking |
| **Settings** | Set display name, theme preference, view data usage, or clear all data |

---

## Requirements

- **Python 3.8+**
- No external packages — uses only the Python standard library (`json`, `os`, `datetime`, `re`, `random`)

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/PaperTrail.git
cd PaperTrail
```

2. Run the app:

```bash
python main.py
```

That's it. No `pip install` needed.

---

## Usage

When you launch PaperTrail, you'll see the main menu:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
         Papertrail
     Learn • Organize • Recall
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Version: v0.1.0

1. Notes
2. Flashcards
3. Quiz Generator
4. AI Summary
5. Daily Planner
6. Settings
7. Help
8. Exit

Choose an option:
```

Pick a number to open that module. Each module has its own sub-menu. Choose **Back** to return to the main menu.

### Quick start workflow

1. **Notes** → Add a few study notes with titles and content
2. **AI Summary** → Summarize a saved note to get a shorter version
3. **Quiz Generator** → Auto-generate a quiz from your notes, then take it
4. **Flashcards** → Create a deck and add question/answer cards for review
5. **Daily Planner** → Schedule study tasks with dates and priorities

---

## Project Structure

```
PaperTrail/
├── main.py              # Entry point — main menu and navigation
├── notes.py             # Notes manager
├── flashcard.py         # Flashcard decks and review
├── quiz_generator.py    # Quiz creation and taking
├── ai_summary.py        # Offline text summarization
├── daily_planner.py     # Task planner
├── setting.py           # App settings and data utilities
├── data/                # Local JSON storage (auto-created)
│   ├── notes.json
│   ├── flashcards.json
│   ├── quizzes.json
│   ├── summaries.json
│   ├── planner.json
│   └── settings.json
└── README.md
```

Each feature lives in its own file and can also be run standalone for testing:

```bash
python notes.py
python flashcard.py
python quiz_generator.py
```

---

## Data Storage

All data is saved locally as JSON files inside the `data/` folder. Nothing is sent to the internet.

| File | Contents |
|------|----------|
| `notes.json` | Your notes (title, content, category, timestamps) |
| `flashcards.json` | Flashcard decks and cards with review stats |
| `quizzes.json` | Multiple-choice quizzes and questions |
| `summaries.json` | Saved text summaries |
| `planner.json` | Daily planner tasks |
| `settings.json` | Display name and theme preference |

Files are created automatically the first time you save something in each module. You can view file sizes in **Settings → Data Usage**, or wipe everything with **Settings → Clear All Data** (type `DELETE` to confirm).

---

## Module Details

### Notes

- Categories: Study, Personal, Work, Ideas
- Search by keyword across title, content, and category
- View a summary showing note counts per category

### Flashcards

- Organize cards into named decks
- Review mode shuffles cards and tracks how often you get each one right
- Per-card stats: correct and incorrect counts

### Quiz Generator

- **Manual:** Build quizzes with 4 options per question
- **Auto-generate:** Creates fill-in-the-blank questions from your saved notes
- Take quizzes with shuffled questions and get a score plus a review of missed answers

### AI Summary

- Runs entirely offline — no API key or internet needed
- Uses word-frequency sentence scoring to pick the most important sentences
- Summarize pasted text or any saved note
- Optionally save summaries for later

### Daily Planner

- Tasks with title, description, date, time, and priority (High / Medium / Low)
- View all tasks, today's tasks, or filter by priority
- Toggle tasks between Pending and Done
- Summary shows total, completed, pending, and due today

### Settings

- Set a display name and theme preference (Light / Dark)
- View all data files and their sizes
- Clear all PaperTrail data with confirmation

---

## Keyboard Shortcuts

| Action | Key |
|--------|-----|
| Exit the app | Choose `8` from the main menu, or press `Ctrl+C` |

---

## Troubleshooting

**"No notes found" when auto-generating a quiz**  
Add notes with longer content. The quiz generator needs words of 5+ letters and enough words across notes to build distractor options.

**Settings not loading**  
Make sure the file is named `settings.json` (with an **s**), not `setting.json`, inside the `data/` folder.

**Data folder missing**  
It is created automatically when you first save a note, task, or any other item.

---

## Contributing

Contributions are welcome. Feel free to open an issue or submit a pull request.

---

## License

This project is open source. Add a license file if you plan to share or publish it publicly.

---

## Acknowledgments

Built as a personal study tool — simple, offline, and focused on learning.
