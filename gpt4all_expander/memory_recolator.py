
# memory_recolator.py
import json
from typing import Any, Dict, Optional

class MemoryRecolator:
    """Manages a JSON-based memory system for saving and recalling key-value pairs."""
    
    def __init__(self, memory_file: str = 'memory.json') -> None:
        """Initialize the MemoryRecolator with the given memory file."""
        self.memory_file = memory_file
        self.load_memory()

    def load_memory(self) -> None:
        """Load the memory from the file into a dictionary."""
        try:
            with open(self.memory_file, 'r') as file:
                self.memory = json.load(file)
        except FileNotFoundError:
            self.memory = {}

    def save_memory(self) -> None:
        """Save the current memory to the file."""
        with open(self.memory_file, 'w') as file:
            json.dump(self.memory, file)

    def add_memory(self, key: str, value: Any) -> None:
        """Add a key-value pair to the memory and save it."""
        self.memory[key] = value
        self.save_memory()

    def recall_memory(self, key: str) -> Optional[Any]:
        """Recall a value from the memory using the given key."""
        return self.memory.get(key, None)
