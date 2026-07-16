from notes import notes_menu
from flashcard import flashcard_menu
from quiz_generator import quiz_generator_menu
from ai_summary import ai_summary_menu
from daily_planner import daily_planner_menu
from setting import setting_menu

APP_NAME = "Papertrail"
VERSION = "v0.1.0"
AUTHOR = "Parth K"

def show_menu():
    print("━" * 40)
    print(f"         {APP_NAME}")
    print(f"     Learn • Organize • Recall")
    print("━" * 40)
    print(f"Version: {VERSION}")
    print()
    print("1. Notes")
    print("2. Flashcards")
    print("3. Quiz Generator")
    print("4. AI Summary")
    print("5. Daily Planner")
    print("6. Exit")
    print("7. Settings")
    print("8. Help")
    print()

def main():
    while True:
        show_menu()

        choice = input("Choose an option: ")

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
            print("\nGoodbye! 👋")
            break

        elif choice == "7":
            setting_menu()

        else:
            print("\nInvalid choice. Please try again.\n") 
            break 

if __name__ == "__main__":
    main()

