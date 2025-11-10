import json
from core.user import User
import time
import os
from core.utils import get_memory_file_path

class GameMemory:

    def __init__(self):
        self.memory = {}
        self.last_save_timestamp = time.time()
        self.memory_file = get_memory_file_path()
        
    def write(self, key: str, value: any):
        self.memory[key] = value
        self.last_save_timestamp = time.time()

    def read(self, key: str) -> any:
        return self.memory.get(key)

    def save(self):         
        self.last_save_timestamp = time.time()
        # Serialize objects to dictionary before saving
        serializable_memory = {}
        for key, value in self.memory.items():
            if isinstance(value, User):
                serializable_memory[key] = {
                    '__type__': 'User',
                    'data': value.to_dict()
                }
            else:
                serializable_memory[key] = value
        
        with open(self.memory_file, "w") as f:
            json.dump(serializable_memory, f, indent=2)

    def load(self):
        if not os.path.exists(self.memory_file):
            self.memory = {}
            return
        
        try:
            with open(self.memory_file, "r") as f:
                loaded_memory = json.load(f)
            
            # Deserialize objects from dictionary
            self.memory = {}
            self.last_save_timestamp = time.time()
            for key, value in loaded_memory.items():
                if isinstance(value, dict) and value.get('__type__') == 'User':
                    self.memory[key] = User.from_dict(value['data'])
                else:
                    self.memory[key] = value
        except (FileNotFoundError, json.JSONDecodeError):
            # If file doesn't exist or is empty/malformed, start with empty memory
            self.memory = {}