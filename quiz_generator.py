"""
PaperTrail Quiz Generator
Build multiple-choice quizzes by hand, or auto-generate simple
fill-in-the-blank quizzes from your existing Notes. Take quizzes
and get scored with a review of what you missed.
"""

import json
import os
import random
import re
from datetime import datetime

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "quizzes.json")
NOTES_FILE = os.path.join(DATA_DIR, "notes.json")

# Common short words skipped when picking a word to blank out
STOPWORDS = {
    "the", "and", "for", "are", "but", "not", "you", "all", "can", "her",
    "was", "one", "our", "out", "day", "get", "has", "him", "his", "how",
    "man", "new", "now", "old", "see", "two", "way", "who", "boy", "did",
    "its", "let", "put", "say", "she", "too", "use", "with", "this",
    "that", "have", "from", "they", "will", "your", "about", "there",
    "which", "when", "what", "into", "than", "them", "then", "were",
    "been", "would", "could", "should", "these", "those", "some",
}

quizzes = []


# ----------------------------- Persistence ----------------------------- #

def load_quizzes():
    global quizzes

    if not os.path.exists(DATA_FILE):
        quizzes = []
        return

    try:
        with open(DATA_FILE, "r") as file:
            quizzes = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        quizzes = []
    except OSError as e:
        print(f"\n❌ Couldn't read quizzes file: {e}\n")
        quizzes = []


def save_quizzes():
    os.makedirs(DATA_DIR, exist_ok=True)
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(quizzes, file, indent=4)
    except OSError as e:
        print(f"\n❌ Couldn't save quizzes: {e}\n")


def load_notes_pool():
    """Read notes.json (owned by the Notes module) if it exists."""
    if not os.path.exists(NOTES_FILE):
        return []
    try:
        with open(NOTES_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []


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


def list_quizzes():
    if len(quizzes) == 0:
        print("\n❌ No quizzes found. Create or generate one first.\n")
        return False

    print("\n📝 Quizzes\n")
    for index, quiz in enumerate(quizzes, start=1):
        q_count = len(quiz["questions"])
        print(f"{index}. {quiz['title']}  ({q_count} question{'s' if q_count != 1 else ''})")
    print()
    return True


def choose_quiz(prompt_text="Choose a quiz number: "):
    if not list_quizzes():
        return None

    index = get_valid_index(quizzes, prompt_text)
    if index is None:
        return None

    return quizzes[index]


# --------------------------- Manual quiz build --------------------------- #

def create_quiz_manual():
    title = prompt_nonempty("Enter quiz title: ")
    questions = []

    print("\nAdd questions one at a time. Leave the question blank to finish.\n")

    while True:
        question_text = input("Question (blank to finish): ").strip()
        if not question_text:
            break

        options = []
        for i in range(1, 5):
            option = prompt_nonempty(f"  Option {i}: ")
            options.append(option)

        while True:
            try:
                correct = int(input("  Which option number is correct? (1-4): "))
                if 1 <= correct <= 4:
                    break
            except ValueError:
                pass
            print("  ❌ Enter a number from 1 to 4.")

        questions.append({
            "question": question_text,
            "options": options,
            "answer_index": correct - 1,
        })
        print("  ✅ Question added.\n")

    if not questions:
        print("\n❌ No questions added — quiz not saved.\n")
        return

    quizzes.append({
        "title": title,
        "questions": questions,
        "source": "manual",
        "created_at": datetime.now().strftime("%d-%m-%Y %I:%M %p"),
    })
    save_quizzes()
    print(f"\n✅ Quiz '{title}' created with {len(questions)} question(s)!\n")


# --------------------------- Auto quiz build ----------------------------- #

def extract_candidate_words(text):
    words = re.findall(r"[A-Za-z]{5,}", text)
    return [w for w in words if w.lower() not in STOPWORDS]


def generate_quiz_from_notes():
    notes_pool = load_notes_pool()

    if not notes_pool:
        print("\n❌ No notes found. Add some notes first (Notes menu), then try again.\n")
        return

    # Build a shared pool of "interesting" words across all notes, used as
    # wrong-answer distractors for whichever note's word gets blanked out.
    all_words = set()
    for note in notes_pool:
        all_words.update(extract_candidate_words(note.get("content", "")))

    questions = []

    for note in notes_pool:
        content = note.get("content", "")
        candidates = extract_candidate_words(content)

        if not candidates:
            continue

        target_word = random.choice(candidates)

        # Build the blanked sentence by replacing the first occurrence
        pattern = re.compile(re.escape(target_word), re.IGNORECASE)
        blanked = pattern.sub("_____", content, count=1)

        distractor_pool = list(all_words - {target_word})
        random.shuffle(distractor_pool)
        distractors = distractor_pool[:3]

        # Not enough distractors in a tiny note collection — skip this one
        if len(distractors) < 3:
            continue

        options = distractors + [target_word]
        random.shuffle(options)

        questions.append({
            "question": f"[{note.get('title', 'Note')}] Fill in the blank: {blanked}",
            "options": options,
            "answer_index": options.index(target_word),
        })

    if not questions:
        print("\n❌ Not enough note content to generate a quiz yet. Add a few more detailed notes.\n")
        return

    title = f"Auto Quiz — {datetime.now().strftime('%d-%m-%Y %H:%M')}"
    quizzes.append({
        "title": title,
        "questions": questions,
        "source": "auto-from-notes",
        "created_at": datetime.now().strftime("%d-%m-%Y %I:%M %p"),
    })
    save_quizzes()
    print(f"\n✅ Generated '{title}' with {len(questions)} question(s) from your notes!\n")


# -------------------------------- Take quiz ------------------------------- #

def take_quiz():
    quiz = choose_quiz("Choose a quiz to take: ")
    if quiz is None:
        return

    questions = quiz["questions"][:]
    random.shuffle(questions)

    score = 0
    missed = []

    print(f"\n📝 {quiz['title']} — {len(questions)} question(s)\n")

    for i, q in enumerate(questions, start=1):
        print(f"({i}/{len(questions)}) {q['question']}")
        for opt_index, option in enumerate(q["options"], start=1):
            print(f"  {opt_index}. {option}")

        try:
            answer = int(input("Your answer: ")) - 1
        except ValueError:
            answer = -1

        if answer == q["answer_index"]:
            print("✅ Correct!\n")
            score += 1
        else:
            correct_option = q["options"][q["answer_index"]]
            print(f"❌ Incorrect. Correct answer: {correct_option}\n")
            missed.append((q["question"], correct_option))

    percent = round((score / len(questions)) * 100) if questions else 0
    print(f"🏁 Score: {score}/{len(questions)} ({percent}%)\n")

    if missed:
        print("Review what you missed:")
        for question, correct_option in missed:
            print(f"  • {question}\n    ✅ Answer: {correct_option}")
        print()


def delete_quiz():
    quiz = choose_quiz("Choose a quiz to delete: ")
    if quiz is None:
        return

    confirm = input(f"Delete quiz '{quiz['title']}'? (y/n): ").strip().lower()
    if confirm != "y":
        print("\nCancelled.\n")
        return

    quizzes.remove(quiz)
    save_quizzes()
    print("\n✅ Quiz deleted.\n")


def view_quiz():
    quiz = choose_quiz("Choose a quiz to view: ")
    if quiz is None:
        return

    print(f"\n📝 {quiz['title']}  ({quiz.get('source', 'manual')})\n")
    for index, q in enumerate(quiz["questions"], start=1):
        print(f"{index}. {q['question']}")
        for opt_index, option in enumerate(q["options"], start=1):
            marker = "✅" if opt_index - 1 == q["answer_index"] else " "
            print(f"   {marker} {opt_index}. {option}")
        print()


# --------------------------------- Menu ---------------------------------- #

def quiz_generator_menu():
    load_quizzes()

    while True:
        print("\n" + "=" * 40)
        print("       📝 PaperTrail Quiz Generator")
        print("=" * 40)
        print("1. Create Quiz Manually")
        print("2. Auto-Generate Quiz from Notes")
        print("3. Take a Quiz")
        print("4. View Quiz (with answers)")
        print("5. Delete Quiz")
        print("6. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_quiz_manual()
        elif choice == "2":
            generate_quiz_from_notes()
        elif choice == "3":
            take_quiz()
        elif choice == "4":
            view_quiz()
        elif choice == "5":
            delete_quiz()
        elif choice == "6":
            print("\nReturning to Main Menu...\n")
            break
        else:
            print("\n❌ Invalid Choice.\n")


if __name__ == "__main__":
    quiz_generator_menu()