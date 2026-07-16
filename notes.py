notes = []


def notes_menu():
    while True:
        print("\n" + "=" * 40)
        print("       📒 PaperTrail Notes")
        print("=" * 40)
        print("1. Add Note")
        print("2. View Notes")
        print("3. Delete Note")
        print("4. Search Note")
        print("5. Back")
        print()

        choice = input("Choose an option: ")

        if choice == "1":

            title = input("Enter Title: ")
            content = input("Enter Content: ")

            note = {
                "title": title,
                "content": content
            }

            notes.append(note)

            print("\n✅ Note Added Successfully!\n")

        elif choice == "2":

            if len(notes) == 0:
                print("\n❌ No notes found.\n")

            else:
                print("\n📚 Your Notes\n")

                for index, note in enumerate(notes, start=1):
                    print(f"Note {index}")
                    print(f"Title   : {note['title']}")
                    print(f"Content : {note['content']}")
                    print("-" * 40)

        elif choice == "3":
            print("\n🗑️ Delete Note (Coming Soon)\n")

        elif choice == "4":
            print("\n🔍 Search Note (Coming Soon)\n")

        elif choice == "5":
            print("\nReturning to Main Menu...\n")
            break

        else:
            print("\n❌ Invalid Choice.\n")