import json
import sqlite3
from task import Task

def clear():
    pass
    


#--------------------------DATABASE CREATION ----------------------------#
def db_connect():
    # Create or connect to a SQLite database file
    connection = sqlite3.connect('task_roll_game.db')
    cursor = connection.cursor()

    #Define the table schema

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY, 
        description TEXT,
        status TEXT,
        start_time REAL,
        end_time REAL,
        category TEXT,
        notes TEXT,
        difficulty INTEGER,
        due_date TEXT
    )
    '''
    # Create the table if it doesn't exist
    cursor.execute(create_table_query)
    return cursor


#-----------------------SAVING-------------------------------
def save_tasks_to_file(tasks, file_path):
    task_data = []
    for task in tasks:
        task_data.append({
            "description": task.description,
            "status": task.status,
            "start_time": task.start_time,
            "end_time": task.end_time,
            "category": task.category,
            "notes": task.notes,
            "difficulty": task.difficulty,
            "due_date": task.due_date
        })
    with open(file_path, 'w') as file:
        json.dump(task_data, file, indent=4)
#-------------------LOADING---------------------------------
def load_tasks_from_file(file_path):
    tasks = []
    with open(file_path, 'r') as file:
        task_data  = json.load(file)
        for task_info in task_data:
            task= Task(task_info["description"], task_info["status"])
            task.start_time = task_info["start_time"]
            task.end_time = task_info["end_time"]
            task.category = task_info["category"]
            task.notes = task_info["notes"]
            task.difficulty = task_info["difficulty"]
            task.due_date = task_info["due_date"]
            tasks.append(task)
    return tasks
