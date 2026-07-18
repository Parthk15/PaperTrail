from notes import notes_menu
from flashcard import flashcard_menu
from quiz_generator import quiz_generator_menu
from ai_summary import ai_summary_menu
from daily_planner import daily_planner_menu
from setting import setting_menu

APP_NAME = "Papertrail"
VERSION = "v0.1.0"
AUTHOR = "Parth K"

MENU_OPTIONS = {
    "1": "Notes",
    "2": "Flashcards",
    "3": "Quiz Generator",
    "4": "AI Summary",
    "5": "Daily Planner",
    "6": "Settings",
    "7": "Help",
    "8": "Exit",
}


def show_menu():
    print("━" * 40)
    print(f"         {APP_NAME}")
    print("     Learn • Organize • Recall")
    print("━" * 40)
    print(f"Version: {VERSION}")
    print()
    for key, label in MENU_OPTIONS.items():
        print(f"{key}. {label}")
    print()


def show_help():
    print("\n" + "━" * 40)
    print(f"         {APP_NAME} Help")
    print("━" * 40)
    print("Notes           - Create, edit, search, and organize notes")
    print("Flashcards      - Build and review flashcard decks")
    print("Quiz Generator  - Turn your notes into practice quizzes")
    print("AI Summary      - Summarize long notes or material")
    print("Daily Planner   - Plan and track your study schedule")
    print("Settings        - Configure app preferences")
    print()
    print(f"{APP_NAME} {VERSION} — made by {AUTHOR}")
    print("━" * 40 + "\n")


def main():
    while True:
        show_menu()

        choice = input("Choose an option: ").strip()

        if choice == "1":
            notes_menu()

        elif choice == "2":
            flashcard_menu()

        elif choice == "3":
            quiz_generator_menu()

        elif choice == "4":
            ai_summary_menu()

        elif choice == "5":
            daily_planner_menu()

        elif choice == "6":
            setting_menu()

        elif choice == "7":
            show_help()

        elif choice == "8":
            print("\nGoodbye! 👋")
            break

        else:
            print("\nInvalid choice. Please try again.\n")
            # no break here — an invalid choice should just re-show the menu,
            # not exit the whole app


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋")