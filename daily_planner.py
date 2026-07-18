"""
PaperTrail Daily Planner
A simple CLI task planner: add, view, edit, delete, complete,
and filter tasks by date or priority.
"""

import json
import os
from datetime import datetime

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "planner.json")

PRIORITIES = {
    "1": "High",
    "2": "Medium",
    "3": "Low",
}

DATE_FORMAT = "%d-%m-%Y"

tasks = []


# ----------------------------- Persistence ----------------------------- #

def load_tasks():
    """Load tasks from disk into the global `tasks` list."""
    global tasks

    if not os.path.exists(DATA_FILE):
        tasks = []
        return

    try:
        with open(DATA_FILE, "r") as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []
    except OSError as e:
        print(f"\n❌ Couldn't read planner file: {e}\n")
        tasks = []


def save_tasks():
    """Persist the global `tasks` list to disk."""
    os.makedirs(DATA_DIR, exist_ok=True)

    try:
        with open(DATA_FILE, "w") as file:
            json.dump(tasks, file, indent=4)
    except OSError as e:
        print(f"\n❌ Couldn't save planner: {e}\n")


# ------------------------------- Helpers -------------------------------- #

def prompt_nonempty(label):
    """Keep asking until the user provides a non-blank string."""
    while True:
        value = input(label).strip()
        if value:
            return value
        print("❌ This can't be empty.")


def prompt_date(label, allow_blank=False, default_today=False):
    """
    Ask for a date in DD-MM-YYYY format, validating it.
    If allow_blank, an empty input returns None (or today's date if
    default_today is True).
    """
    while True:
        raw = input(label).strip()

        if not raw:
            if default_today:
                return datetime.now().strftime(DATE_FORMAT)
            if allow_blank:
                return None
            print("❌ This can't be empty.")
            continue

        try:
            datetime.strptime(raw, DATE_FORMAT)
            return raw
        except ValueError:
            print("❌ Please use DD-MM-YYYY format (e.g. 18-07-2026).")


def prompt_time(label):
    """Ask for an optional time string. No strict validation, just trims."""
    return input(label).strip()


def choose_priority():
    print("\nSelect Priority")
    print("1. High")
    print("2. Medium")
    print("3. Low")

    choice = input("Enter choice: ").strip()
    return PRIORITIES.get(choice, "Medium")


def print_task(index, task):
    status = "✅ Done" if task.get("status") == "Done" else "⏳ Pending"
    time_str = f" {task['time']}" if task.get("time") else ""

    print(f"Task {index}")
    print(f"Title    : {task['title']}")
    if task.get("description"):
        print(f"Details  : {task['description']}")
    print(f"Date     : {task.get('date', 'No date')}{time_str}")
    print(f"Priority : {task.get('priority', 'Medium')}")
    print(f"Status   : {status}")
    print("-" * 40)


def get_valid_index(prompt_text):
    """Ask for a task number and return a valid 0-based index, or None."""
    try:
        task_number = int(input(prompt_text))
    except ValueError:
        print("\n❌ Please enter a valid number.\n")
        return None

    if 1 <= task_number <= len(tasks):
        return task_number - 1

    print("\n❌ Invalid task number.\n")
    return None


def sort_key(task):
    """Sort by date, then time, undated tasks last."""
    date_str = task.get("date")
    try:
        date_val = datetime.strptime(date_str, DATE_FORMAT) if date_str else datetime.max
    except ValueError:
        date_val = datetime.max
    return (date_val, task.get("time") or "")


# -------------------------------- Actions -------------------------------- #

def add_task():
    title = prompt_nonempty("Enter Task Title: ")
    description = input("Enter Details (optional): ").strip()
    date = prompt_date("Enter Date (DD-MM-YYYY, blank for today): ", default_today=True)
    time = prompt_time("Enter Time (optional, e.g. 05:30 PM): ")
    priority = choose_priority()

    task = {
        "title": title,
        "description": description,
        "date": date,
        "time": time,
        "priority": priority,
        "status": "Pending",
        "created_at": datetime.now().strftime("%d-%m-%Y %I:%M %p"),
    }

    tasks.append(task)
    save_tasks()

    print("\n✅ Task Added Successfully!\n")


def view_tasks(task_list=None, header="🗓️  Your Tasks"):
    task_list = tasks if task_list is None else task_list

    if len(task_list) == 0:
        print("\n❌ No tasks found.\n")
        return

    ordered = sorted(task_list, key=sort_key)

    print(f"\n{header}\n")
    for index, task in enumerate(ordered, start=1):
        print_task(index, task)


def view_today():
    today = datetime.now().strftime(DATE_FORMAT)
    todays_tasks = [t for t in tasks if t.get("date") == today]
    view_tasks(todays_tasks, header=f"📅 Today's Tasks ({today})")


def view_by_priority():
    if len(tasks) == 0:
        print("\n❌ No tasks found.\n")
        return

    priority = choose_priority()
    filtered = [t for t in tasks if t.get("priority", "Medium") == priority]
    view_tasks(filtered, header=f"⭐ {priority} Priority Tasks")


def toggle_complete():
    if len(tasks) == 0:
        print("\n❌ No tasks available.\n")
        return

    view_tasks()

    index = get_valid_index("\nEnter task number to toggle complete/pending: ")
    if index is None:
        return

    task = tasks[index]
    task["status"] = "Pending" if task.get("status") == "Done" else "Done"
    save_tasks()

    print(f"\n✅ '{task['title']}' marked as {task['status']}!\n")


def edit_task():
    if len(tasks) == 0:
        print("\n❌ No tasks available.\n")
        return

    view_tasks()

    index = get_valid_index("\nEnter task number to edit: ")
    if index is None:
        return

    task = tasks[index]

    print("\nCurrent Details")
    print_task(index + 1, task)

    print("Leave blank to keep the current value.")
    new_title = input("New title: ").strip()
    new_description = input("New details: ").strip()
    new_date = prompt_date("New date (DD-MM-YYYY): ", allow_blank=True)
    new_time = input("New time: ").strip()
    change_priority = input("Change priority? (y/n): ").strip().lower()

    if new_title:
        task["title"] = new_title
    if new_description:
        task["description"] = new_description
    if new_date:
        task["date"] = new_date
    if new_time:
        task["time"] = new_time
    if change_priority == "y":
        task["priority"] = choose_priority()

    task["updated_at"] = datetime.now().strftime("%d-%m-%Y %I:%M %p")

    save_tasks()
    print("\n✅ Task Updated Successfully!\n")


def delete_task():
    if len(tasks) == 0:
        print("\n❌ No tasks to delete.\n")
        return

    view_tasks()

    index = get_valid_index("\nEnter task number to delete: ")
    if index is None:
        return

    confirm = input(f"Delete '{tasks[index]['title']}'? (y/n): ").strip().lower()
    if confirm != "y":
        print("\nCancelled.\n")
        return

    deleted_task = tasks.pop(index)
    save_tasks()

    print(f"\n✅ '{deleted_task['title']}' deleted successfully!\n")


def show_summary():
    if len(tasks) == 0:
        print("\n❌ No tasks found.\n")
        return

    done = sum(1 for t in tasks if t.get("status") == "Done")
    pending = len(tasks) - done
    today = datetime.now().strftime(DATE_FORMAT)
    due_today = sum(1 for t in tasks if t.get("date") == today and t.get("status") != "Done")

    print("\n📊 Planner Summary")
    print(f"Total tasks  : {len(tasks)}")
    print(f"Completed    : {done}")
    print(f"Pending      : {pending}")
    print(f"Due today    : {due_today}")
    print()


# --------------------------------- Menu ---------------------------------- #

def daily_planner_menu():
    load_tasks()

    while True:
        print("\n" + "=" * 40)
        print("       🗓️  PaperTrail Daily Planner")
        print("=" * 40)
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. View Today's Tasks")
        print("4. Mark Complete / Pending")
        print("5. Edit Task")
        print("6. Delete Task")
        print("7. View by Priority")
        print("8. Summary")
        print("9. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            view_today()
        elif choice == "4":
            toggle_complete()
        elif choice == "5":
            edit_task()
        elif choice == "6":
            delete_task()
        elif choice == "7":
            view_by_priority()
        elif choice == "8":
            show_summary()
        elif choice == "9":
            print("\nReturning to Main Menu...\n")
            break
        else:
            print("\n❌ Invalid Choice.\n")


if __name__ == "__main__":
    daily_planner_menu()