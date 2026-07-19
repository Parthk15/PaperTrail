"""
PaperTrail Settings
App-wide preferences (display name, theme label) plus utilities to
locate or clear your stored data.
"""

import json
import os

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "settings.json")

DEFAULT_SETTINGS = {
    "display_name": "",
    "theme": "Light",
}

DATA_FILES_BY_MODULE = {
    "Notes": "notes.json",
    "Flashcards": "flashcards.json",
    "Quiz Generator": "quizzes.json",
    "AI Summary": "summaries.json",
    "Daily Planner": "planner.json",
    "Settings": "settings.json",
}

settings = dict(DEFAULT_SETTINGS)


# ----------------------------- Persistence ----------------------------- #

def load_settings():
    global settings

    if not os.path.exists(DATA_FILE):
        settings = dict(DEFAULT_SETTINGS)
        return

    try:
        with open(DATA_FILE, "r") as file:
            loaded = json.load(file)
            settings = {**DEFAULT_SETTINGS, **loaded}
    except (FileNotFoundError, json.JSONDecodeError):
        settings = dict(DEFAULT_SETTINGS)
    except OSError as e:
        print(f"\n❌ Couldn't read settings file: {e}\n")
        settings = dict(DEFAULT_SETTINGS)


def save_settings():
    os.makedirs(DATA_DIR, exist_ok=True)
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(settings, file, indent=4)
    except OSError as e:
        print(f"\n❌ Couldn't save settings: {e}\n")


# -------------------------------- Actions -------------------------------- #

def view_settings():
    print("\n⚙️  Current Settings\n")
    name = settings.get("display_name") or "(not set)"
    print(f"Display Name : {name}")
    print(f"Theme        : {settings.get('theme', 'Light')}")
    print(f"Data Folder  : {os.path.abspath(DATA_DIR)}")
    print()


def edit_display_name():
    current = settings.get("display_name") or "(not set)"
    new_name = input(f"Enter display name [{current}]: ").strip()

    if new_name:
        settings["display_name"] = new_name
        save_settings()
        print("\n✅ Display name updated!\n")
    else:
        print("\nNo change made.\n")


def toggle_theme():
    settings["theme"] = "Dark" if settings.get("theme") == "Light" else "Light"
    save_settings()
    print(f"\n✅ Theme set to {settings['theme']}!\n")
    print("Note: this app is terminal-based, so 'theme' is just a saved")
    print("preference for now — it doesn't change how output looks here.\n")


def show_data_usage():
    print("\n📂 Data Files\n")
    if not os.path.exists(DATA_DIR):
        print("No data folder found yet — nothing has been saved.\n")
        return

    for module_name, filename in DATA_FILES_BY_MODULE.items():
        path = os.path.join(DATA_DIR, filename)
        if os.path.exists(path):
            size_kb = os.path.getsize(path) / 1024
            print(f"  {module_name:<15} {filename:<18} {size_kb:.1f} KB")
        else:
            print(f"  {module_name:<15} {filename:<18} (not created yet)")
    print()


def clear_all_data():
    print("\n⚠️  This will permanently delete ALL PaperTrail data:")
    print("   notes, flashcards, quizzes, summaries, planner tasks, and settings.\n")

    confirm = input("Type 'DELETE' to confirm, anything else to cancel: ").strip()
    if confirm != "DELETE":
        print("\nCancelled — nothing was deleted.\n")
        return

    if not os.path.exists(DATA_DIR):
        print("\nNo data to delete.\n")
        return

    deleted_any = False
    for filename in DATA_FILES_BY_MODULE.values():
        path = os.path.join(DATA_DIR, filename)
        if os.path.exists(path):
            try:
                os.remove(path)
                deleted_any = True
            except OSError as e:
                print(f"❌ Couldn't delete {filename}: {e}")

    global settings
    settings = dict(DEFAULT_SETTINGS)

    if deleted_any:
        print("\n✅ All PaperTrail data has been cleared.\n")
    else:
        print("\nNothing was there to delete.\n")


def show_about():
    print("\n" + "━" * 40)
    print("         Papertrail")
    print("     Learn • Organize • Recall")
    print("━" * 40)
    print("Version : v0.1.0")
    print("Author  : Parth K")
    print("A lightweight offline study companion: notes, flashcards,")
    print("quizzes, note summaries, and a daily planner — all local,")
    print("no account or internet connection required.")
    print("━" * 40 + "\n")


# --------------------------------- Menu ---------------------------------- #

def setting_menu():
    load_settings()

    while True:
        print("\n" + "=" * 40)
        print("       ⚙️  PaperTrail Settings")
        print("=" * 40)
        print("1. View Settings")
        print("2. Edit Display Name")
        print("3. Toggle Theme (Light/Dark)")
        print("4. Data Usage")
        print("5. Clear All Data")
        print("6. About")
        print("7. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_settings()
        elif choice == "2":
            edit_display_name()
        elif choice == "3":
            toggle_theme()
        elif choice == "4":
            show_data_usage()
        elif choice == "5":
            clear_all_data()
        elif choice == "6":
            show_about()
        elif choice == "7":
            print("\nReturning to Main Menu...\n")
            break
        else:
            print("\n❌ Invalid Choice.\n")


if __name__ == "__main__":
    setting_menu()