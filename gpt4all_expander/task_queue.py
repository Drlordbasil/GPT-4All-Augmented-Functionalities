from collections import deque

class TaskQueue:
    def __init__(self):
        self.queue = deque()

    def add_task(self, task):
        self.queue.append(task)

    def get_next_task(self):
        return self.queue.popleft() if self.queue else None
