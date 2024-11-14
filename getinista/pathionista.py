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

    print("\nAvailable Firefox Profiles:")
    for i, profile in enumerate(profiles):
        profile_name = os.path.basename(profile)
        session_dir = profile / 'sessionstore-backups'
        session_files = _find_session_files(profile)

        num_sessions = len(session_files)
        print(f"{i + 1}: {profile_name}")
        print(f"   Number of session files: {num_sessions}")
    while True:
        try:
            choice = int(input("\nEnter the profile number (or 0 to exit): ")) - 1
            if choice == -1:
                print("Exiting.")
                sys.exit(0)
            if 0 <= choice < len(profiles):
                return profiles[choice]
            else:
                print("Invalid selection, please choose a number between 1 and", len(profiles))
        except ValueError:
            print("Please enter a valid number.")

def _find_session_files(profile_path):
    session_store_backups = profile_path / "sessionstore-backups"
    if not session_store_backups.exists():
        return []
    
    # Find all *.jsonlz4 files
    session_files = list(session_store_backups.glob("*.jsonlz4"))
    
    # Separate current session 'recovery.jsonlz4' and others
    current_session = []
    backup_sessions = []
    for file in session_files:
        if file.name.startswith("recovery"):
            current_session.append(file)
        else:
            backup_sessions.append(file)
    
    # Order: current session first, then backups
    ordered_sessions = current_session + backup_sessions
    return ordered_sessions

def _ask_session_file(session_files):
    if not session_files:
        print("No session files found.")
        return None

    print("\nAvailable session files:")
    for i, file in enumerate(session_files):
        if file.name.startswith("recovery"):
            label = "Current Session"
        elif file.name.startswith("previous"):
            label = "Previous Session"
        elif file.name.startswith("upgrade"):
            label = "Upgrade Session"
        else:
            label = "Backup Session"
        print(f"{i + 1}: {file.name} ({label})")

    # Ask user to select a session file
    while True:
        try:
            choice = int(input("\nEnter the session file number (or 0 to cancel): ")) - 1
            if choice == -1:
                print("Cancelled session selection.")
                return None
            if 0 <= choice < len(session_files):
                selected_file = session_files[choice]
                print(f"\nSelected session file: {selected_file}")
                return selected_file
            else:
                print("Invalid selection, please choose a number between 1 and", len(session_files))
        except ValueError:
            print("Please enter a valid number.")

def get_session_file():
    profiles = _find_firefox_profiles()

    if not profiles:
        print("No Firefox profiles found.")
        return

    selected_profile = _ask_profile(profiles)
    if not selected_profile:
        print("No profile selected.")
        return

    session_files = _find_session_files(selected_profile)

    if session_files:
        selected_session = _ask_session_file(session_files)
        if selected_session:
            return selected_session
        else:
            print("No session file selected.")
            return None
    else:
        print("No session files found in the selected profile.")
        return None
