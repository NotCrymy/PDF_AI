import json
from pathlib import Path

class DocumentLoader:
    """
    A class for loading JSON documents from a specified directory.
    """
    def __init__(self, directory: str):
        self.directory = Path(directory)

    def load_all(self):
        """
        Loads all JSON documents from the specified directory and returns them as a list of dictionaries.
        
        Returns:
            list: A list of dictionaries representing the loaded JSON documents.
        """
        documents = []

        if not self.directory.exists() or not self.directory.is_dir():
            self.directory.mkdir(parents=True, exist_ok=True)
            print(f"Directory {self.directory} created.")

        for file_path in self.directory.glob("*.json"):
            with open(file_path, "r", encoding="utf-8") as f:
                document = json.load(f)

            documents.append(document)

        return documents