import json
import os

class SessionManager:
    _instance = None
    _file_path = "session.json"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
            cls._instance.data = cls._load_from_file()
        return cls._instance

    @classmethod
    def _load_from_file(cls):
        """Load session data from the JSON file."""
        if os.path.exists(cls._file_path):
            try:
                with open(cls._file_path, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def _save_to_file(self):
        """Save session data to the JSON file."""
        with open(self._file_path, "w") as f:
            json.dump(self.data, f, indent=4)

    def set(self, key, value):
        """Store a value in the session and persist it."""
        self.data[key] = value
        self._save_to_file()

    def get(self, key):
        """Retrieve a value from the session."""
        return self.data.get(key, None)

    def clear(self):
        """Clear the session data and remove the file."""
        self.data = {}
        if os.path.exists(self._file_path):
            os.remove(self._file_path)