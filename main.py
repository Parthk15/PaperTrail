def show_menu():
    print("━" * 40)
    print(f"         {PAPER TRAIL}")
    print(f"     {Learn • Organize • Recall}")
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
            print("\nOpening Notes...\n")

        elif choice == "2":
            print("\nOpening Flashcards...\n")

        elif choice == "3":
            print("\nOpening Quiz Generator...\n")

        elif choice == "4":
            print("\nOpening AI Summary...\n")

        elif choice == "5":
            print("\nOpening Daily Planner...\n")

        elif choice == "6":
            print("\nGoodbye! 👋")
            break

        elif choice == "7":
            print("\nOpening Settings...\n")

        elif choice == "8":
            print("\nOpening Help...\n")

        else:
            print("\nInvalid choice. Please try again.\n") 
            break 

if __name__ == "__main__":
    main()

