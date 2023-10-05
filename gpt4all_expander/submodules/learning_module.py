# File: gpt4all_expander/submodules/learning_module.py

import os
import json

class LearningModule:
    def __init__(self, data_file='learning_data.json'):
        self.data_file = data_file
        self.load_data()

    def load_data(self) -> None:
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                self.data = json.load(file)
        else:
            self.data = {"learning_iterations": 0, "generated_data": []}

    def save_data(self) -> None:
        with open(self.data_file, 'w') as file:
            json.dump(self.data, file, indent=4)

    def learn(self, generated_data: list) -> None:
        self.data["learning_iterations"] += 1
        self.data["generated_data"].extend(generated_data)
        self.save_data()