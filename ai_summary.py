"""
PaperTrail AI Summary
Summarizes text using a lightweight extractive algorithm (word-frequency
sentence scoring) that runs entirely offline — no API key required.
Can summarize pasted text or any note you've already saved.
"""

import json
import os
import re
from datetime import datetime

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "summaries.json")
NOTES_FILE = os.path.join(DATA_DIR, "notes.json")

STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "then", "so", "to", "of",
    "in", "on", "at", "for", "with", "by", "from", "as", "is", "are",
    "was", "were", "be", "been", "being", "it", "its", "this", "that",
    "these", "those", "i", "you", "he", "she", "we", "they", "them",
    "his", "her", "their", "our", "your", "my", "not", "no", "do", "does",
    "did", "can", "could", "will", "would", "should", "may", "might",
    "have", "has", "had", "there", "here", "than", "into", "about",
    "up", "down", "out", "over", "under", "again", "such", "also",
}

summaries = []


# ----------------------------- Persistence ----------------------------- #

def load_summaries():
    global summaries

    if not os.path.exists(DATA_FILE):
        summaries = []
        return

    try:
        with open(DATA_FILE, "r") as file:
            summaries = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        summaries = []
    except OSError as e:
        print(f"\n❌ Couldn't read summaries file: {e}\n")
        summaries = []


def save_summaries():
    os.makedirs(DATA_DIR, exist_ok=True)
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(summaries, file, indent=4)
    except OSError as e:
        print(f"\n❌ Couldn't save summaries: {e}\n")


def load_notes_pool():
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


def read_multiline(label):
    """Collect multi-line input, ending on a blank line."""
    print(f"{label} (finish with an empty line):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines)


# ------------------------------ Summarizer ------------------------------- #

def split_sentences(text):
    text = text.strip()
    if not text:
        return []
    # Split on sentence-ending punctuation, keep it simple and dependency-free
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if s.strip()]


def word_frequencies(text):
    words = re.findall(r"[A-Za-z']+", text.lower())
    freq = {}
    for word in words:
        if word in STOPWORDS or len(word) < 3:
            continue
        freq[word] = freq.get(word, 0) + 1
    return freq


def summarize_text(text, num_sentences=3):
    sentences = split_sentences(text)

    if len(sentences) <= num_sentences:
        return sentences  # nothing to trim

    freq = word_frequencies(text)
    if not freq:
        return sentences[:num_sentences]

    max_freq = max(freq.values())
    normalized = {word: count / max_freq for word, count in freq.items()}

    scores = []
    for index, sentence in enumerate(sentences):
        words = re.findall(r"[A-Za-z']+", sentence.lower())
        score = sum(normalized.get(w, 0) for w in words)
        # Slight bonus for earlier sentences (often carry the main idea)
        score += (len(sentences) - index) * 0.01
        scores.append((score, index, sentence))

    top = sorted(scores, key=lambda x: x[0], reverse=True)[:num_sentences]
    top_in_order = sorted(top, key=lambda x: x[1])  # restore original order

    return [s for _, _, s in top_in_order]


# -------------------------------- Actions -------------------------------- #

def summarize_new_text():
    text = read_multiline("Paste or type the text to summarize")
    if not text.strip():
        print("\n❌ No text provided.\n")
        return

    num_sentences = ask_sentence_count(text)
    summary_lines = summarize_text(text, num_sentences)
    summary = " ".join(summary_lines)

    print("\n🧾 Summary\n")
    print(summary)
    print()

    save = input("Save this summary? (y/n): ").strip().lower()
    if save == "y":
        title = prompt_nonempty("Title for this summary: ")
        store_summary(title, text, summary)


def summarize_saved_note():
    notes_pool = load_notes_pool()

    if not notes_pool:
        print("\n❌ No notes found. Add some notes first (Notes menu).\n")
        return

    print("\n📚 Your Notes\n")
    for index, note in enumerate(notes_pool, start=1):
        print(f"{index}. {note.get('title', 'Untitled')}")
    print()

    index = get_valid_index(notes_pool, "Choose a note to summarize: ")
    if index is None:
        return

    note = notes_pool[index]
    text = note.get("content", "")

    if not text.strip():
        print("\n❌ That note has no content.\n")
        return

    num_sentences = ask_sentence_count(text)
    summary_lines = summarize_text(text, num_sentences)
    summary = " ".join(summary_lines)

    print(f"\n🧾 Summary of '{note.get('title', 'Untitled')}'\n")
    print(summary)
    print()

    save = input("Save this summary? (y/n): ").strip().lower()
    if save == "y":
        store_summary(note.get("title", "Untitled"), text, summary)


def ask_sentence_count(text):
    sentence_total = len(split_sentences(text))
    default = min(3, sentence_total) or 1

    raw = input(f"How many sentences in the summary? (default {default}): ").strip()
    if not raw:
        return default

    try:
        value = int(raw)
        return max(1, value)
    except ValueError:
        print(f"❌ Invalid number, using default ({default}).")
        return default


def store_summary(title, original_text, summary):
    summaries.append({
        "title": title,
        "original_length_chars": len(original_text),
        "summary": summary,
        "created_at": datetime.now().strftime("%d-%m-%Y %I:%M %p"),
    })
    save_summaries()
    print("\n✅ Summary saved!\n")


def view_summaries():
    if len(summaries) == 0:
        print("\n❌ No saved summaries yet.\n")
        return

    print("\n🧾 Saved Summaries\n")
    for index, s in enumerate(summaries, start=1):
        print(f"{index}. {s['title']}  ({s.get('created_at', 'Unknown')})")
        print(f"   {s['summary']}")
        print("-" * 40)


def delete_summary():
    if len(summaries) == 0:
        print("\n❌ No saved summaries yet.\n")
        return

    view_summaries()
    index = get_valid_index(summaries, "\nEnter summary number to delete: ")
    if index is None:
        return

    removed = summaries.pop(index)
    save_summaries()
    print(f"\n✅ Deleted summary '{removed['title']}'.\n")


# --------------------------------- Menu ---------------------------------- #

def ai_summary_menu():
    load_summaries()

    while True:
        print("\n" + "=" * 40)
        print("       🤖 PaperTrail AI Summary")
        print("=" * 40)
        print("1. Summarize New Text")
        print("2. Summarize a Saved Note")
        print("3. View Saved Summaries")
        print("4. Delete Summary")
        print("5. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            summarize_new_text()
        elif choice == "2":
            summarize_saved_note()
        elif choice == "3":
            view_summaries()
        elif choice == "4":
            delete_summary()
        elif choice == "5":
            print("\nReturning to Main Menu...\n")
            break
        else:
            print("\n❌ Invalid Choice.\n")


if __name__ == "__main__":
    ai_summary_menu()