"""
PaperTrail Notes
A simple CLI notes manager: add, view, edit, delete, search, filter,
and get a quick summary of your notes.
"""

import json
import os
from datetime import datetime

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "notes.json")

CATEGORIES = {
    "1": "Study",
    "2": "Personal",
    "3": "Work",
    "4": "Ideas",
}

notes = []


# ----------------------------- Persistence ----------------------------- #

def load_notes():
    """Load notes from disk into the global `notes` list."""
    global notes

    if not os.path.exists(DATA_FILE):
        notes = []
        return

    try:
        with open(DATA_FILE, "r") as file:
            notes = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        notes = []
    except OSError as e:
        print(f"\n❌ Couldn't read notes file: {e}\n")
        notes = []


def save_notes():
    """Persist the global `notes` list to disk."""
    os.makedirs(DATA_DIR, exist_ok=True)

    try:
        with open(DATA_FILE, "w") as file:
            json.dump(notes, file, indent=4)
    except OSError as e:
        print(f"\n❌ Couldn't save notes: {e}\n")


# ------------------------------- Helpers -------------------------------- #

def prompt_nonempty(label):
    """Keep asking until the user provides a non-blank string."""
    while True:
        value = input(label).strip()
        if value:
            return value
        print("❌ This can't be empty.")


def choose_category():
    print("\nSelect Category")
    print("1. Study")
    print("2. Personal")
    print("3. Work")
    print("4. Ideas")

    choice = input("Enter choice: ").strip()
    return CATEGORIES.get(choice, "Others")


def print_note(index, note):
    print(f"Note {index}")
    print(f"Title   : {note['title']}")
    print(f"Content : {note['content']}")
    print(f"Category: {note.get('category', 'Others')}")
    print(f"Created : {note.get('created_at', 'Unknown')}")
    print("-" * 40)


def get_valid_index(prompt_text):
    """Ask for a note number and return a valid 0-based index, or None."""
    try:
        note_number = int(input(prompt_text))
    except ValueError:
        print("\n❌ Please enter a valid number.\n")
        return None

    if 1 <= note_number <= len(notes):
        return note_number - 1

    print("\n❌ Invalid note number.\n")
    return None


# -------------------------------- Actions -------------------------------- #

def add_note():
    title = prompt_nonempty("Enter Title: ")
    content = prompt_nonempty("Enter Content: ")
    category = choose_category()

    note = {
        "title": title,
        "content": content,
        "category": category,
        "created_at": datetime.now().strftime("%d-%m-%Y %I:%M %p"),
    }

    notes.append(note)
    save_notes()

    print("\n✅ Note Added Successfully!\n")


def view_notes(note_list=None, header="📚 Your Notes"):
    note_list = notes if note_list is None else note_list

    if len(note_list) == 0:
        print("\n❌ No notes found.\n")
        return

    print(f"\n{header}\n")

    for index, note in enumerate(note_list, start=1):
        print_note(index, note)


def view_by_category():
    if len(notes) == 0:
        print("\n❌ No notes found.\n")
        return

    category = choose_category()
    filtered = [n for n in notes if n.get("category", "Others") == category]

    view_notes(filtered, header=f"📂 {category} Notes")


def delete_note():
    if len(notes) == 0:
        print("\n❌ No notes to delete.\n")
        return

    view_notes()

    index = get_valid_index("\nEnter note number to delete: ")
    if index is None:
        return

    confirm = input(f"Delete '{notes[index]['title']}'? (y/n): ").strip().lower()
    if confirm != "y":
        print("\nCancelled.\n")
        return

    deleted_note = notes.pop(index)
    save_notes()

    print(f"\n✅ '{deleted_note['title']}' deleted successfully!\n")


def search_note():
    if len(notes) == 0:
        print("\n❌ No notes found.\n")
        return

    keyword = input("Enter keyword: ").strip().lower()
    if not keyword:
        print("\n❌ Please enter a keyword.\n")
        return

    found = False
    print()

    for index, note in enumerate(notes, start=1):
        if (
            keyword in note["title"].lower()
            or keyword in note["content"].lower()
            or keyword in note.get("category", "").lower()
        ):
            print_note(index, note)
            found = True

    if not found:
        print("❌ No matching notes found.\n")


def edit_note():
    if len(notes) == 0:
        print("\n❌ No notes available.\n")
        return

    view_notes()

    index = get_valid_index("\nEnter note number to edit: ")
    if index is None:
        return

    note = notes[index]

    print("\nCurrent Details")
    print(f"Title   : {note['title']}")
    print(f"Content : {note['content']}")
    print(f"Category: {note.get('category', 'Others')}")

    print("\nLeave blank to keep the current value.")
    new_title = input("New title: ").strip()
    new_content = input("New content: ").strip()
    change_category = input("Change category? (y/n): ").strip().lower()

    if new_title:
        note["title"] = new_title
    if new_content:
        note["content"] = new_content
    if change_category == "y":
        note["category"] = choose_category()

    note["updated_at"] = datetime.now().strftime("%d-%m-%Y %I:%M %p")

    save_notes()
    print("\n✅ Note Updated Successfully!\n")


def show_summary():
    if len(notes) == 0:
        print("\n❌ No notes found.\n")
        return

    counts = {}
    for note in notes:
        category = note.get("category", "Others")
        counts[category] = counts.get(category, 0) + 1

    print("\n📊 Notes Summary")
    print(f"Total notes: {len(notes)}")
    for category, count in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {category:<10}: {count}")
    print()


# --------------------------------- Menu ---------------------------------- #

def notes_menu():
    load_notes()

    while True:
        print("\n" + "=" * 40)
        print("       📒 PaperTrail Notes")
        print("=" * 40)
        print("1. Add Note")
        print("2. View Notes")
        print("3. Delete Note")
        print("4. Search Note")
        print("5. Edit Note")
        print("6. View by Category")
        print("7. Summary")
        print("8. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_note()
        elif choice == "2":
            view_notes()
        elif choice == "3":
            delete_note()
        elif choice == "4":
            search_note()
        elif choice == "5":
            edit_note()
        elif choice == "6":
            view_by_category()
        elif choice == "7":
            show_summary()
        elif choice == "8":
            print("\nReturning to Main Menu...\n")
            break
        else:
            print("\n❌ Invalid Choice.\n")


if __name__ == "__main__":
    notes_menu()
