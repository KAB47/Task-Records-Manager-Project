import os
from datetime import datetime

TASKS_FILE = 'tasks.txt'

def create_user_file():
    """
    Create the user.txt file if it doesn't exist.
    Optionally adds an admin user account to start.
    """
    if not os.path.exists('user.txt'):
        with open('user.txt', 'w') as file:
            # Optional: Add an initial admin account
            file.write("admin,admin123\n")
        print("user.txt file created with an initial admin account.")
    else:
        print("user.txt file already exists.")

def register_user():
    """
    Register a new user by adding their username and password to the user.txt file.
    Prompts the user to enter a new username and password.
    Checks if the username already exists and notifies the user if it does.
    """
    username = input("Enter a new username: ").strip()
    password = input("Enter a password: ").strip()

    # Check if user.txt exists, if not, create it
    if not os.path.exists('user.txt'):
        create_user_file()

    # Read existing users
    with open('user.txt', 'r') as file:
        existing_users = [line.strip().split(',') for line in file.readlines()]

    # Check for duplicate username
    for user in existing_users:
        if username == user[0].strip():
            print("Username already exists. Please choose a different username.")
            return

    # Register new user
    with open('user.txt', 'a') as file:
        file.write(f"{username},{password}\n")

    print(f"User '{username}' registered successfully.")

def login_user():
    """
    Login a user by checking their username and password against user.txt.
    """
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    if not os.path.exists('user.txt'):
        print("No registered users found. Please register first.")
        return

    with open('user.txt', 'r') as file:
        existing_users = [line.strip().split(',') for line in file.readlines()]

    for user in existing_users:
        stored_username = user[0].strip()
        stored_password = user[1].strip()

        if username == stored_username and password == stored_password:
            print(f"Welcome back, {username}!")
            return username

    print("Incorrect username or password. Please try again.")
    return None

def view_all_tasks():
    """
    Display all tasks from the tasks.txt file.
    """
    if not os.path.exists(TASKS_FILE):
        print("No tasks found.")
        return

    with open(TASKS_FILE, 'r') as file:
        lines = file.readlines()

    if not lines:
        print("No tasks found.")
        return

    print("All Tasks:")
    for i, line in enumerate(lines, start=1):
        task_data = line.strip().split(', ')
        if len(task_data) == 7:
            assigner, assignee, title, description, due_date, assigned_date, completed = task_data
            completion_status = "Yes" if completed.lower() == 'true' else "No"
            print(
                f"{i}. Assigner: {assigner}, Assignee: {assignee}, "
                f"Title: {title}, Description: {description}, "
                f"Due Date: {due_date}, Assigned Date: {assigned_date}, "
                f"Completed: {completion_status}"
            )
        else:
            print(f"Invalid task data format in line {i}.")

def add_task(current_user):
    """
    Add a new task to the tasks.txt file.
    """
    assign_to = input("Enter the username of the person to whom the task should be assigned: ")

    with open('user.txt', 'r') as file:
        users = [line.strip().split(',')[0] for line in file.readlines()]

    if assign_to not in users:
        print(f"User '{assign_to}' does not exist. Please enter a valid username.")
        return

    title = input("Enter task title: ")
    description = input("Enter task description: ")
    due_date = input("Enter due date (YYYY-MM-DD): ")
    assigned_date = datetime.now().strftime("%Y-%m-%d")
    completed = input("Is the task completed? (Yes/No): ").lower() == 'yes'

    task_details = f"{current_user}, {assign_to}, {title}, {description}, {due_date}, {assigned_date}, {completed}\n"

    with open(TASKS_FILE, 'a') as file:
        file.write(task_details)

    print(f"Task assigned to '{assign_to}' and added successfully.")

def view_my_tasks(current_user):
    """
    Display tasks assigned to the current user from the tasks.txt file.
    """
    if not os.path.exists(TASKS_FILE):
        print("No tasks found.")
        return

    with open(TASKS_FILE, 'r') as file:
        lines = file.readlines()

    if not lines:
        print("No tasks found.")
        return

    print("Your Tasks:")
    my_tasks = [line for line in lines if line.strip().split(', ')[1] == current_user]

    for i, line in enumerate(my_tasks, start=1):
        task_data = line.strip().split(', ')
        if len(task_data) == 7:
            assigner, assignee, title, description, due_date, assigned_date, completed = task_data
            completion_status = "Yes" if completed.lower() == 'true' else "No"
            print(
                f"{i}. Assigner: {assigner}, "
                f"Title: {title}, Description: {description}, "
                f"Due Date: {due_date}, Assigned Date: {assigned_date}, "
                f"Completed: {completion_status}"
            )
        else:
            print(f"Invalid task data format in line {i}.")

def main():
    """
    Main function to run the task management system.
    Displays the initial login or register menu.
    """
    # Create the user.txt file when the program starts
    create_user_file()

    while True:
        print("\nPlease select one of the following options:")
        print("l - Login")
        print("r - Register User")
        print("e - Exit")

        user_input = input("Enter your choice: ").strip().lower()

        if user_input == 'l':
            current_user = login_user()
            if current_user:
                print(f"Login successful! Welcome to the task management system.")
                # Main menu options
                while True:
                    print("\nMain Menu:")
                    print("a - Add Task")
                    print("va - View All Tasks")
                    print("vm - View My Tasks")
                    print("e - Exit")

                    choice = input("Enter your choice: ").strip().lower()

                    if choice == 'a':
                        add_task(current_user)
                    elif choice == 'va':
                        view_all_tasks()
                    elif choice == 'vm':
                        view_my_tasks(current_user)
                    elif choice == 'e':
                        print("Exiting the program. Goodbye!")
                        return
                    else:
                        print("Invalid choice. Please try again.")
        elif user_input == 'r':
            register_user()
        elif user_input == 'e':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
