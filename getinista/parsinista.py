import os
import json
import lz4.block

MAGIC_NUMBER = b"mozLz40\0"  # it's not a number, but if you think about it hard enough it is


def decompress_session_file(file_path: str) -> dict:
    with open(file_path, "rb") as f:
        magic = f.read(8)
        if magic != MAGIC_NUMBER:
            raise ValueError("Invalid firefox sessionstore file format.")
        json_data = lz4.block.decompress(f.read())
        session = json.loads(json_data)
        return session

def simplify_session_data(session):
    simplified_data = []
    for window_idx, window in enumerate(session.get("windows", []), start=1):
        window_data = {"tabs": []}
        for tab_idx, tab in enumerate(window.get("tabs", []), start=1):
            entries = []
            for entry_idx, entry in enumerate(tab.get("entries", []), start=1):
                entry_id = f"{window_idx}:{tab_idx}:{entry_idx}"
                entries.append({
                    "id": entry_id,
                    "title": entry.get("title", ""),
                    "url": entry.get("url", "")
                })
            window_data["tabs"].append(entries)
        simplified_data.append(window_data)
    return simplified_data

class FileExistsError(Exception):
    def __init__(self, message="File already exists. Please choose a different path"):
        self.message = message
        super().__init__(self.message)

class Parsinista():
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.session_data = None

    def save_simplified_session(self):
        if os.path.exists(self.output_file):
            raise FileExistsError
        if not self.session_data:
            raise ValueError
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(self.session_data, f, ensure_ascii=False, indent=2)
        print(f"Session is saved to {self.output_file}")

    def convert_and_save_session(self):
        decompressed = decompress_session_file(self.input_file)
        self.session_data = simplify_session_data(decompressed)
        self.save_simplified_session()
