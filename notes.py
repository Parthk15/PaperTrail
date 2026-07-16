import json

notes = []


def load_notes():
    global notes

    try:
        with open("data/notes.json", "r") as file:
            notes = json.load(file)

    except FileNotFoundError:
        notes = []

    except json.JSONDecodeError:
        notes = []


def save_notes():
    with open("data/notes.json", "w") as file:
        json.dump(notes, file, indent=4)


def add_note():
    title = input("Enter Title: ")
    content = input("Enter Content: ")

    note = {
        "title": title,
        "content": content
    }

    notes.append(note)
    save_notes()

    print("\n✅ Note Added Successfully!\n")


def view_notes():
    if len(notes) == 0:
        print("\n❌ No notes found.\n")
        return

    print("\n📚 Your Notes\n")

    for index, note in enumerate(notes, start=1):
        print(f"Note {index}")
        print(f"Title   : {note['title']}")
        print(f"Content : {note['content']}")
        print("-" * 40)


def delete_note():
    print("\n🗑️ Delete Note (Coming Soon)\n")


def search_note():
    print("\n🔍 Search Note (Coming Soon)\n")


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
        print("5. Back")
        print()

        choice = input("Choose an option: ")

        if choice == "1":
            add_note()

        elif choice == "2":
            view_notes()

        elif choice == "3":
            delete_note()

        elif choice == "4":
            search_note()

        elif choice == "5":
            print("\nReturning to Main Menu...\n")
            break

        else:
            print("\n❌ Invalid Choice.\n")