import os
import sys
import platform
from pathlib import Path
from dataclasses import dataclass, field

from clinista import get_user_choice

@dataclass
class Session():
    path: Path

@dataclass
class Profile():
    path: Path
    sessions: list[Session] = field(init=False)
    session_number: int = field(init=False)

    def __post_init__(self):
        self.sessions = find_sessions(self.path)
        self.session_number = len(self.sessions)

def _find_firefox_profiles() -> list[Profile]:
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
    profile_paths = list(profiles_path.glob("*"))
    profiles = [Profile(pp) for pp in profile_paths]
    return profiles

def choose_profile(profiles: list[Profile]) -> Profile | None:
    if not profiles:
        print("No Firefox profiles found.")
        return None

    print("\nAvailable Firefox Profiles:")
    options = [f"{p.path.name} | {p.session_number} sessions" for p in profiles]
    choice = get_user_choice(options, "Select a firefox profile")
    if choice is not None:
        return profiles[choice]
    return None

def find_sessions(profile_path: Path) -> list[Session]:
    session_store_backups = profile_path / "sessionstore-backups"
    if not session_store_backups.exists():
        return []
    
    session_files = list(session_store_backups.glob("*.jsonlz4"))
    sessions = [Session(fp) for fp in session_files]
    
    current_session = []
    backup_sessions = []
    for session in sessions:
        if session.path.name.startswith("recovery"):
            current_session.append(session)
        else:
            backup_sessions.append(session)
    
    ordered_sessions = current_session + backup_sessions
    return ordered_sessions

def _create_session_file_label(file: Path) -> str:
    if file.name.startswith("recovery"):
        return "Current Session"
    elif file.name.startswith("previous"):
        return "Previous Session"
    elif file.name.startswith("upgrade"):
        return "Upgrade Session"
    else:
        return "Backup Session"

def choose_session(session_files: list[Session]) -> Session | None:
    if not session_files:
        print("No session files found.")
        return None

    session_labels = [f"{s.path.name} ({_create_session_file_label(s.path)})" for s in session_files]
    choice = get_user_choice(session_labels, "Select a session file")

    if choice is None:
        return None
    selected_session = session_files[choice]
    print(f"\nSelected session file: {selected_session.path}")
    return selected_session

def get_session_file():
    profiles = _find_firefox_profiles()
    if not profiles:
        print("No Firefox profiles found.")
        return
    selected_profile = choose_profile(profiles)
    if not selected_profile:
        print("No profile selected.")
        return
    sessions = find_sessions(selected_profile.path)
    if sessions:
        selected_session = choose_session(sessions)
        if selected_session:
            return selected_session.path
        else:
            print("No session file selected.")
            return None
    else:
        print("No session files found in the selected profile.")
        return None
