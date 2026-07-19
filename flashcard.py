"""
PaperTrail Flashcards
Create decks of question/answer flashcards and review them,
tracking how often you get each card right or wrong.
"""

import json
import os
import random
from datetime import datetime

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "flashcards.json")

decks = []


# ----------------------------- Persistence ----------------------------- #

def load_decks():
    global decks

    if not os.path.exists(DATA_FILE):
        decks = []
        return

    try:
        with open(DATA_FILE, "r") as file:
            decks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        decks = []
    except OSError as e:
        print(f"\n❌ Couldn't read flashcards file: {e}\n")
        decks = []


def save_decks():
    os.makedirs(DATA_DIR, exist_ok=True)
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(decks, file, indent=4)
    except OSError as e:
        print(f"\n❌ Couldn't save flashcards: {e}\n")


# ------------------------------- Helpers -------------------------------- #

def prompt_nonempty(label):
    while True:
        value = input(label).strip()
        if value:
            return value
        print("❌ This can't be empty.")


def get_valid_index(collection, prompt_text):
    try:
        number = int(input(prompt_text))
    except ValueError:
        print("\n❌ Please enter a valid number.\n")
        return None

    if 1 <= number <= len(collection):
        return number - 1

    print("\n❌ Invalid number.\n")
    return None


def list_decks():
    if len(decks) == 0:
        print("\n❌ No decks found. Create one first.\n")
        return False

    print("\n📚 Decks\n")
    for index, deck in enumerate(decks, start=1):
        card_count = len(deck["cards"])
        print(f"{index}. {deck['name']}  ({card_count} card{'s' if card_count != 1 else ''})")
    print()
    return True


def choose_deck(prompt_text="Choose a deck number: "):
    if not list_decks():
        return None

    index = get_valid_index(decks, prompt_text)
    if index is None:
        return None

    return decks[index]


# -------------------------------- Actions -------------------------------- #

def create_deck():
    name = prompt_nonempty("Enter deck name: ")

    if any(d["name"].lower() == name.lower() for d in decks):
        print("\n❌ A deck with that name already exists.\n")
        return

    decks.append({
        "name": name,
        "cards": [],
        "created_at": datetime.now().strftime("%d-%m-%Y %I:%M %p"),
    })
    save_decks()
    print(f"\n✅ Deck '{name}' created!\n")


def delete_deck():
    deck = choose_deck("Choose a deck number to delete: ")
    if deck is None:
        return

    confirm = input(f"Delete deck '{deck['name']}' and all its cards? (y/n): ").strip().lower()
    if confirm != "y":
        print("\nCancelled.\n")
        return

    decks.remove(deck)
    save_decks()
    print(f"\n✅ Deck deleted.\n")


def add_card():
    deck = choose_deck("Choose a deck to add a card to: ")
    if deck is None:
        return

    question = prompt_nonempty("Enter question: ")
    answer = prompt_nonempty("Enter answer: ")

    deck["cards"].append({
        "question": question,
        "answer": answer,
        "correct_count": 0,
        "incorrect_count": 0,
    })
    save_decks()
    print("\n✅ Card added!\n")


def view_deck():
    deck = choose_deck("Choose a deck to view: ")
    if deck is None:
        return

    if len(deck["cards"]) == 0:
        print(f"\n❌ '{deck['name']}' has no cards yet.\n")
        return

    print(f"\n📖 {deck['name']}\n")
    for index, card in enumerate(deck["cards"], start=1):
        print(f"Card {index}")
        print(f"Q: {card['question']}")
        print(f"A: {card['answer']}")
        print(f"Stats: ✅ {card['correct_count']}  ❌ {card['incorrect_count']}")
        print("-" * 40)


def edit_card():
    deck = choose_deck("Choose a deck: ")
    if deck is None:
        return

    if len(deck["cards"]) == 0:
        print(f"\n❌ '{deck['name']}' has no cards yet.\n")
        return

    view_deck_cards(deck)
    index = get_valid_index(deck["cards"], "Enter card number to edit: ")
    if index is None:
        return

    card = deck["cards"][index]

    print("\nLeave blank to keep the current value.")
    new_question = input(f"New question [{card['question']}]: ").strip()
    new_answer = input(f"New answer [{card['answer']}]: ").strip()

    if new_question:
        card["question"] = new_question
    if new_answer:
        card["answer"] = new_answer

    save_decks()
    print("\n✅ Card updated!\n")


def view_deck_cards(deck):
    print(f"\n📖 {deck['name']}\n")
    for index, card in enumerate(deck["cards"], start=1):
        print(f"{index}. {card['question']}")
    print()


def delete_card():
    deck = choose_deck("Choose a deck: ")
    if deck is None:
        return

    if len(deck["cards"]) == 0:
        print(f"\n❌ '{deck['name']}' has no cards yet.\n")
        return

    view_deck_cards(deck)
    index = get_valid_index(deck["cards"], "Enter card number to delete: ")
    if index is None:
        return

    removed = deck["cards"].pop(index)
    save_decks()
    print(f"\n✅ Removed card: {removed['question']}\n")


def review_deck():
    deck = choose_deck("Choose a deck to review: ")
    if deck is None:
        return

    if len(deck["cards"]) == 0:
        print(f"\n❌ '{deck['name']}' has no cards yet.\n")
        return

    order = deck["cards"][:]
    random.shuffle(order)

    correct = 0
    incorrect = 0

    print(f"\n🧠 Reviewing '{deck['name']}' — {len(order)} card(s)")
    print("Press Enter to reveal each answer.\n")

    for i, card in enumerate(order, start=1):
        print(f"({i}/{len(order)}) Q: {card['question']}")
        input("Press Enter to reveal answer...")
        print(f"A: {card['answer']}")

        result = input("Did you get it right? (y/n): ").strip().lower()
        if result == "y":
            card["correct_count"] += 1
            correct += 1
        else:
            card["incorrect_count"] += 1
            incorrect += 1
        print("-" * 40)

    save_decks()

    print(f"\n🏁 Review complete! ✅ {correct} correct, ❌ {incorrect} incorrect.\n")


def show_summary():
    if len(decks) == 0:
        print("\n❌ No decks found.\n")
        return

    print("\n📊 Flashcard Summary")
    total_cards = 0
    for deck in decks:
        cards = deck["cards"]
        total_cards += len(cards)
        correct = sum(c["correct_count"] for c in cards)
        incorrect = sum(c["incorrect_count"] for c in cards)
        print(f"  {deck['name']:<20} {len(cards)} card(s)  ✅ {correct}  ❌ {incorrect}")
    print(f"\nTotal decks: {len(decks)}  Total cards: {total_cards}\n")


# --------------------------------- Menu ---------------------------------- #

def flashcard_menu():
    load_decks()

    while True:
        print("\n" + "=" * 40)
        print("       🧠 PaperTrail Flashcards")
        print("=" * 40)
        print("1. Create Deck")
        print("2. Add Card")
        print("3. View Deck")
        print("4. Review Deck")
        print("5. Edit Card")
        print("6. Delete Card")
        print("7. Delete Deck")
        print("8. Summary")
        print("9. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_deck()
        elif choice == "2":
            add_card()
        elif choice == "3":
            view_deck()
        elif choice == "4":
            review_deck()
        elif choice == "5":
            edit_card()
        elif choice == "6":
            delete_card()
        elif choice == "7":
            delete_deck()
        elif choice == "8":
            show_summary()
        elif choice == "9":
            print("\nReturning to Main Menu...\n")
            break
        else:
            print("\n❌ Invalid Choice.\n")


if __name__ == "__main__":
    flashcard_menu()