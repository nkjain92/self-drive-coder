import json
import os
import threading
import time
from context_analysis import analyze_project_structure

class ProjectState:
    def __init__(self, save_interval=300):
        self.conversation_history = []
        self.file_structure = self.get_file_structure()
        self.save_interval = save_interval
        self.last_save_time = time.time()
        self.start_auto_save()

    def add_to_history(self, message):
        if message.get('content'):  # Only add non-empty messages
            self.conversation_history.append(message)
            self.check_auto_save()

    def update_file_structure(self):
        self.file_structure = self.get_file_structure()
        self.check_auto_save()

    def get_file_structure(self):
        return analyze_project_structure()

    def save(self):
        state = {
            "conversation_history": self.conversation_history,
            "file_structure": self.file_structure
        }
        with open("project_state.json", "w") as f:
            json.dump(state, f)
        self.last_save_time = time.time()

    def load(self):
        if os.path.exists("project_state.json"):
            with open("project_state.json", "r") as f:
                state = json.load(f)
            self.conversation_history = state["conversation_history"]
            self.file_structure = state["file_structure"]

    def check_auto_save(self):
        if time.time() - self.last_save_time >= self.save_interval:
            self.save()

    def start_auto_save(self):
        def auto_save():
            while True:
                time.sleep(self.save_interval)
                self.save()

        threading.Thread(target=auto_save, daemon=True).start()