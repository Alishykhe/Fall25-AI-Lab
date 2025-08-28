import os

#This is file path
FILE_PATH = "tasks.txt"

#Load tasks from file
def load_tasks():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []

def save_tasks(tasks):
    with open(FILE_PATH, "w") as f:
        for task in tasks:
            f.write(task + "\n")

def show_menu():
    print("--- To Do List ---")
    print("1. Add Task")
    print("2. Show Tasks")
    print("3. Remove Task")
    print("4. Exit")

def add_task(tasks):
    task = input("Enter new task: ")
    tasks.append(task)
    save_tasks(tasks) #save tasks in file
    print(f"Added: {task}")

def show_tasks(tasks):
    if not tasks:
        print("No tasks.")
    else:
        print("Your Tasks:")
        for i, task in enumerate(tasks, start=1):
            print(f"{i}. {task}")

def remove_task(tasks):
    show_tasks(tasks)
    if tasks:
        try:
            num = int(input("Enter task number to remove: "))
            if 1 <= num <= len(tasks):
                removed = tasks.pop(num - 1)
                save_tasks(tasks)   # update file after removing
                print(f"Removed: {removed}")
            else:
                print("Invalid task number.")
        except ValueError:
            print("Please enter a number only.")

# Main loop
def main():
    tasks = load_tasks()
    while True:
        show_menu()
        choice = input("Choose option: ")

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            show_tasks(tasks)
        elif choice == "3":
            remove_task(tasks)
        elif choice == "4":
            print("Exited...")
            break
        else:
            print("Invalid choice, try again.")

main()