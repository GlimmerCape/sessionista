import os
import json
from typing import Callable
import lz4.block

from clinista import ask_for_valid_input

MAGIC_NUMBER = b"mozLz40\0"  # it's not a number


def decompress_session_file(file_path: str) -> dict:
    with open(file_path, "rb") as f:
        magic = f.read(8)
        if magic != MAGIC_NUMBER:
            raise ValueError("Invalid firefox sessionstore file format.")
        json_data = lz4.block.decompress(f.read())
        session = json.loads(json_data)
        return session

def is_valid_yn_answer(user_input: str) -> bool:
    if user_input == 'y' or user_input == 'n':
        return True
    print("Invalid input. Expected either 'y' or 'n'")
    return False

def pick_windows(data: list[dict]) -> None:
    idx = 0
    while idx < len(data):
        print("Save this window? 5 tabs from the window(chosen randomly(actually not)):")
        for tab in data[idx]['tabs'][-5:]:
            print(f"    title: {tab[-1]['title']}")
            print(f"    url: {tab[-1]['url']}")
        user_input = ask_for_valid_input("y/n:", is_valid_yn_answer)
        if user_input == 'y':
            idx += 1
        else:
            print('Not saving the window above')
            data.pop(idx)

def process_session_data(session, post_process_func: Callable[[list[dict]], None] | None=None) -> list[dict]:
    simplified_data = []
    for window_idx, window in enumerate(session.get("windows", []), start=1):
        window_data = {"tabs": [], "tab_count": 0}
        tab_count = 0
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
            tab_count += 1
        window_data["tab_count"] = tab_count
        simplified_data.append(window_data)
    if post_process_func:
        post_process_func(simplified_data)
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
        for window in self.session_data:
            print("Window with " + str(window["tab_count"]) + " tabs")
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(self.session_data, f, ensure_ascii=False, indent=2)
        print(f"Session is saved to {self.output_file}")

    def convert_and_save_session(self, choose_windows_to_save: bool=False):
        decompressed = decompress_session_file(self.input_file)
        post_process_func = pick_windows if choose_windows_to_save else None
        self.session_data = process_session_data(decompressed, post_process_func)
        self.save_simplified_session()

if __name__ == "__main__":
    data = [
        {
            "tabs": [
                {"title": "first", "url": "first_url"},
                {"title": "second", "url": "second_url"},
                {"title": "third", "url": "third_url"},
            ]
        },
        {
            "tabs": [
                {"title": "1", "url": "first_url"},
                {"title": "2", "url": "second_url"},
                {"title": "3", "url": "third_url"},
            ]
        },
        {
            "tabs": [
                {"title": "___", "url": "first_url"},
                {"title": "___", "url": "second_url"},
                {"title": "___", "url": "third_url"},
            ]
        },
    ]
    print(data)
    pick_windows(data)
    print(data)
