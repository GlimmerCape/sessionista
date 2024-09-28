import os
import sys
import glob
from pathlib import Path


def find_firefox_profiles():
    # Detect OS and set Firefox profiles path
    if sys.platform == "win32":
        base_path = Path(os.getenv("APPDATA")) / "Mozilla" / "Firefox" / "Profiles"
    elif sys.platform == "darwin":
        base_path = Path.home() / "Library" / "Application Support" / "Firefox" / "Profiles"
    elif sys.platform == "linux":
        base_path = Path.home() / ".mozilla" / "firefox"
    else:
        print("Unsupported OS")
        return None

    profiles = list(base_path.glob("*.default*"))
    return profiles


def ask_profile(profiles):
    print("Available Firefox Profiles:")
    for i, profile in enumerate(profiles):
        print(f"{i + 1}: {profile}")

    # Ask user to select a profile
    while True:
        try:
            choice = int(input("Enter the profile number: ")) - 1
            if 0 <= choice < len(profiles):
                return profiles[choice]
            else:
                print("Invalid selection, please choose again.")
        except ValueError:
            print("Please enter a valid number.")


def find_session_files(profile_path):
    session_files = glob.glob(str(profile_path / "sessionstore-backups" / "*.jsonlz4"))
    return session_files


def ask_session_file(session_files):
    print("\nAvailable session files:")
    for i, file in enumerate(session_files):
        print(f"{i + 1}: {file}")

    # Ask user to select a session file
    while True:
        try:
            choice = int(input("Enter the session file number: ")) - 1
            if 0 <= choice < len(session_files):
                return session_files[choice]
            else:
                print("Invalid selection, please choose again.")
        except ValueError:
            print("Please enter a valid number.")


def get_session_file():
    profiles = find_firefox_profiles()

    if not profiles:
        print("No Firefox profiles found.")
        return

    selected_profile = ask_profile(profiles)

    session_files = find_session_files(selected_profile)

    if session_files:
        selected_session = ask_session_file(session_files)
        print(f"Selected session file: {selected_session}")
        return selected_session
    else:
        print("No session files found in the selected profile.")
        return None
