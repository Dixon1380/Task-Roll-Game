
import threading
import time 




class Task:
    def __init__(self, description, status='Pending', category="", notes="", difficulty=1, due_date=None):
        self.description = description
        self.status = status
        self.start_time = None
        self.end_time = None
        self.category = category
        self.notes = notes
        self.difficulty = difficulty
        self.due_date = due_date
        self.is_completed = False # Flag to indicate if the task is complete.

    def start_timer(self):
        self.start_time = time.time()
        self.timer_thread = threading.Timer(1.0, self.update_timer)
        self.timer_threadstart()
    
    def update_timer(self):
        try:
            if self.status == "Started":
                elapsed_time = time.time() - self.start_time
                # Update the timer display in the user interface with the elapsed_time
                # You can use a callback function or message queue to update the UI safely

                #Call update_timer again after 1 second (recursive call for continuous updating)

                self.timer_thread = threading.Timer(1.0, self.update_timer)
                self.timer_thread.start()
        except Exception as e:
            # Handle the exception (e.g., log the error, display an error message.)
            print(f"Error in update_timer: {e}")

    def complete_task(self):
        if self.status == "Started":
            self.status = "Completed"
            self.end_time = time.time()
            self.is_completed = True
            completed_time = self.end_time  - self.start_time
            self.complete_tasks.append((self.description, completed_time ))
        self.timer_thread.cancel() # Stops the timer thread when the task is completed.


    def __str__(self):
        return f"Task: {self.description} | Status: {self.status} | Category: {self.category} | Notes: {self.notes} | Difficulty: {self.difficulty} | Due Date: {self.due_date}"