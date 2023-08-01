import random
import threading
import os

import static_funcs as sf
from task import Task



class TaskRollGame:
    def __init__(self):
        self.TASKS = []  # List of Task objects
        self.ASSIGNED_TASKS = {
        }
        self.dice_mode = 1 # Default to one die mode
        self.completed_tasks = [] # List to store completed tasks and their completion times
        self.cursor = sf.db_connect()

    def choose_dice_mode(self):
        print("Choose your dice mode: ")
        print("1: One die")
        print("2: Two dice")
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                self.dice_mode = 1
            elif choice == 2:
                self.dice_mode = 2
            else:
                print("Invalid choice. Using default mode (one die).")
        except ValueError:
            print("Invalid input. Using default mode (one die).")

    def add_task(self):
        number_of_entries = 0
        if self.dice_mode == 1:
           while number_of_entries < 6:
                print(f"Number of task entered: {number_of_entries}\n")  
                description = input("Enter the task description: ")
                category = input("Enter the task category: ")
                notes = input("Enter any notes for the task: ")
                difficulty = int(input("Enter the task difficulty level (1-5, where 1 is easiest and 5 is harder): "))
                due_date = input("Enter the task due date (optional, format: YYYY-MM-DD): ")
                task = Task(description, category=category,notes=notes, difficulty=difficulty, due_date=due_date)
                self.TASKS.append(task)
                print("\n")
                number_of_entries += 1
                print("\n")
        elif self.dice_mode == 2:
            while number_of_entries < 12:
                print(f"Number of task entered: {number_of_entries}\n") 
                description = input("Enter the task description: ")
                category = input("Enter the task category: ")
                notes = input("Enter any notes for the task: ")
                difficulty = int(input("Enter the task difficulty level (1-5, where 1 is easiest and 5 is harder): "))
                due_date = input("Enter the task due date (optional, format: YYYY-MM-DD): ")
                task = Task(description,status="Pending", category=category,notes=notes, difficulty=difficulty, due_date=due_date)
                self.TASKS.append(task)
                print("\n")
                number_of_entries += 1
                print("\n")
        else:
            raise("An error occured when adding tasks.")

    def delete_task(self):
        if not self.TASKS:
            print("No tasks to delete.")
            return

        print("Select a task to delete:")
        for index, task in enumerate(self.TASKS, start=1):
            print(f"{index}: {task.description}")

        try:
            choice = int(input())
            if 1 <= choice <= len(self.TASKS):
                del self.TASKS[choice - 1]
                print("Task deleted.")
            else:
                print("Invalid choice. No task was deleted.")
        except ValueError:
            print("Invalid input. No task was deleted.")

    def modify_task_description(self):
        if not self.TASKS:
            print("No tasks to modify.")
            return

        print("Select a task to modify:")
        for index, task in enumerate(self.TASKS, start=1):
            print(f"{index}: {task.description}")

        try:
            choice = int(input())
            if 1 <= choice <= len(self.TASKS):
                new_description = input("Enter the new task description: ")
                self.TASKS[choice - 1].description = new_description
                print("Task description modified.")
            else:
                print("Invalid choice. No task was modified.")
        except ValueError:
            print("Invalid input. No task was modified.")

    def prioritize_tasks(self):
        print("Assigned priority to tasks from less to most important.")
        for task in self.TASKS:
            print(f"Task: {task.description}")
            try:
                prompt = int(input("Choose a number from (1 to 6) or (1 to 12), if you are in two dice mode: "))
                if 1 <= prompt <= 12:
                    self.ASSIGNED_TASKS[prompt] = task
                else:
                    print("Invalid priority. Task was not assigned.")
            except ValueError:
                print("Invalid input. Task was not assigned.")

        for key, value in self.ASSIGNED_TASKS.items():
            print(f"{key} - {value.description} - Status: {value.status}")

    def update_task_status(self):
        if not self.TASKS:
            print("No tasks to update status.")
            return

        print("Select a task to update status:")
        for index, task in enumerate(self.TASKS, start=1):
            print(f"{index}: {task.description} - Status: {task.status}")

        try:
            choice = int(input())
            if 1 <= choice <= len(self.TASKS):
                print("Select the new status:")
                print("1: Complete")
                print("2: Started")
                print("3: Ended")
                print("4: Pending")
                status_choice = int(input())

                if status_choice == 1:
                    self.TASKS[choice - 1].status = "Completed"
                    self.TASKS[choice - 1].complete_task()
                    self.completed_tasks.append(self.TASKS[choice - 1])
                elif status_choice == 2:
                    self.TASKS[choice - 1].status = "Started"
                    self.TASKS[choice - 1].start_timer()
                elif status_choice == 3:
                    self.TASKS[choice - 1].status = "Ended"
                elif status_choice == 4:
                    self.TASKS[choice - 1].status = "Pending"
                else:
                    print("Invalid choice. Task status was not updated.")
            else:
                print("Invalid choice. Task status was not updated.")
        except ValueError:
            print("Invalid input. Task status was not updated.")

    def show_task_history(self):
        print("Completed Task History:")
        if not self.completed_task:
            print("No completed tasks yet.")
        else:
            for task, completion_time in self.completed_tasks:
                print(f"Task: {task} - Completion Time: {completion_time:.2f} seconds")

    def roll_die(self):
        if self.dice_mode == 1:
            return random.randint(1, 6)
        elif self.dice_mode == 2:
            return random.randint(1,6) + random.randint(1, 6)
        else:
            print("Invalid dice mode. Using default mode (one die).")
            return random.randint(1,6)
    
    def save_tasks_to_database(self):
        # Delete all existing tasks in the database
        db_connection = sf.db_connect()

        delete_query = 'DELETE FROM tasks'
        db_connection.execute(delete_query)

        # Insert or update each task in the database
        for task in self.TASKS:
            insert_query = "INSERT INTO tasks (description, status, start_time, end_time, category, notes, difficulty, due_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            db_connection.execute(insert_query, (task.description, task.status, task.start_time, task.end_time, task.category, task.notes, task.difficulty, task.due_date))

        # Commit the changes and close the connection
        db_connection.connection.commit
        db_connection.connection.close()


    def save_tasks_thread(self):
        save_thread = threading.Thread(target=self.save_tasks_to_database)
        save_thread.start()

    def load_tasks_from_database(self):
        
        select_query = 'SELECT * FROM tasks'
        self.cursor.execute(select_query)

        task_data = self.cursor.fetchall()
        # add the task that are complete to the completed_task list
        for row in task_data:
            task = Task(row[1])  # Assuming the description is in the second column (index 1)
            task.status = row[2]  # Assuming the status is in the third column (index 2)
            task.start_time = row[3]  # Assuming the start_time is in the fourth column (index 3)
            task.end_time = row[4]  # Assuming the end_time is in the fifth column (index 4)
            task.category = row[5] # Assuming the end_time is in the fifth column (index 5)
            task.notes = row[6] # Assuming the end_time is in the sixth column (index 6)
            task.difficulty = row[7] # Assuming the end_time is in the seventh column (index 7)
            task.due_date = row[8] # Assuming the end_time is in the eigth column (index 8)
            self.TASKS.append(task)
        self.cursor.connection.close()
        # load task that are completed to the completed_tasks list
        for task in self.TASKS:
            if task.status == 'Completed':
                self.completed_tasks.append(task)


    def save_game(self):
        file_path = "task_roll_game_save.json" # Choose a suitable file path
        sf.save_tasks_to_file(self.TASKS, file_path)
        print("Game saved successfully")

    def load_game(self):
        file_path = "task_roll_game_save.json" # Choose the same file path used
        if os.path.exists(file_path):
            self.TASKS = sf.load_tasks_from_file(file_path)
        else:
            print("No saved game found.")

        print("Game loaded successfully")

    def main(self):
        print("Welcome to Task Roll!")
        print("Please see Rules in the README to learn how the game works!\n")
        print("Good luck and Have fun!")

        print("\n New or Load Game")
        print("1: New Game")
        print("2: Load Game")
        try:
            choice = int(input("Enter your choice: "))
            
            if choice == 1:
                self.choose_dice_mode()
            elif choice == 2:
                print("Load from JSON or DB file:")
                print("1: Load JSON file")
                print("2: Load DB File")
                try:
                    choice = int(input("Enter your choice: "))
                    if choice == 1:
                        self.load_game()
                    elif choice == 2:
                        self.load_tasks_from_database()
                    else:
                        print("Invalid input. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a vaild number.")
                self.choose_dice_mode()
            else:
                print("Invalid input. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

        is_running = True

        while is_running:
            print("\nMenu:")
            print("1: Add a task")
            print("2: Delete a task")
            print("3: Modify task description")
            print("4: Update task status")
            print("5: Prioritize tasks")
            print("6: Roll the die")
            print("7: Show Task History")
            print("8 Save or Load Game")
            print("9: Exit")
            
            try:
                choice = int(input("Enter your choice: "))

                if choice == 1:
                    self.add_task()
                    self.save_tasks_thread()
                elif choice == 2:
                    self.delete_task()
                    self.save_tasks_thread()
                elif choice == 3:
                    self.modify_task_description()
                    self.save_tasks_thread()
                elif choice == 4:
                    self.update_task_status()
                    self.save_tasks_thread()
                elif choice == 5:
                    self.prioritize_tasks()
                    self.save_tasks_thread()
                elif choice == 6:
                    your_roll = self.roll_die()
                    task = self.ASSIGNED_TASKS[your_roll]
                    if task.status == "Completed":
                        elasped_time = task.end_time - task.start_time
                        print(f"Congratulations! You completed the task in {elasped_time:.2f} seconds.\n")
                    else:
                        print(f"You have landed on {your_roll}!\n")
                        print(f"Your task is:\n {task}")

                elif choice == 7:
                    self.show_task_history()
                elif choice == 8:
                    print("Save or Load Game")
                    print("1: Save Game")
                    print("2: Load Game")
                    try:
                        choice = int(input("Enter your choice: "))
                        if choice == 1:
                            self.save_game()
                            self.save_tasks_thread()
                        elif choice == 2:
                            self.load_game()
                            self.save_tasks_thread()
                        else:
                            print("Invalid input. Please try again")
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")

                    self.save_game()
                elif choice == 9:
                    is_running = False
                    print("Thanks for playing Task Roll! Goodbye!")
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")