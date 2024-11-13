import os
import sys
import glob
import platform
from pathlib import Path

def _find_firefox_profiles():
    if 'microsoft' in platform.release().lower():
        # Running in WSL
        windows_username = input("Enter your Windows username: ")
        profiles_dir = f"/mnt/c/Users/{windows_username}/AppData/Roaming/Mozilla/Firefox/Profiles"
    elif os.name == 'nt':
        # Running on Windows
        appdata = os.getenv('APPDATA')
        profiles_dir = os.path.join(appdata, 'Mozilla', 'Firefox', 'Profiles')
    else:
        # Running on Linux or macOS
        home = os.path.expanduser('~')
        profiles_dir = os.path.join(home, '.mozilla', 'firefox')

    if not os.path.exists(profiles_dir):
        print(f"Firefox profiles directory not found at: {profiles_dir}")
        sys.exit(1)

    profiles_path = Path(profiles_dir)
    profiles = list(profiles_path.glob("*"))
    return profiles


def _ask_profile(profiles):
    if not profiles:
        print("No Firefox profiles found.")
        return None

    print("Available Firefox Profiles:")
    for i, profile in enumerate(profiles):
        profile_name = os.path.basename(profile)
        session_dir = os.path.join(profile, 'sessionstore-backups')
        session_files = []

        if os.path.isdir(session_dir):
            for fname in os.listdir(session_dir):
                fpath = os.path.join(session_dir, fname)
                if os.path.isfile(fpath):
                    session_files.append(fpath)

        num_sessions = len(session_files)

        print(f"{i + 1}: {profile_name}")
        print(f"   Number of session files: {num_sessions}")
    while True:
        try:
            choice = int(input("Enter the profile number: ")) - 1
            if 0 <= choice < len(profiles):
                return profiles[choice]
            else:
                print("Invalid selection, please choose a number between 1 and", len(profiles))
        except ValueError:
            print("Please enter a valid number.")

def _find_session_files(profile_path):
    session_files = glob.glob(str(profile_path / "sessionstore-backups" / "*.jsonlz4"))
    return session_files


def _ask_session_file(session_files):
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
    profiles = _find_firefox_profiles()

    if not profiles:
        print("No Firefox profiles found.")
        return

    selected_profile = _ask_profile(profiles)

    session_files = _find_session_files(selected_profile)

    if session_files:
        selected_session = _ask_session_file(session_files)
        print(f"Selected session file: {selected_session}")
        return selected_session
    else:
        print("No session files found in the selected profile.")
        return None
