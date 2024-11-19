import os
import sys
import platform
import re
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
        self.sessions = _find_sessions(self.path)
        self.session_number = len(self.sessions)

def _find_firefox_profiles(pattern: str='.*') -> list[Profile]:
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

    compiled_pattern = re.compile(pattern)
    profiles = [Profile(pp) for pp in profile_paths if compiled_pattern.match(str(pp))]
    return profiles

def _find_sessions(profile_path: Path, pattern: str='.*') -> list[Session]:
    session_store_backups = profile_path / "sessionstore-backups"
    if not session_store_backups.exists():
        return []
    
    session_files = list(session_store_backups.glob("*.jsonlz4"))
    compiled_pattern = re.compile(pattern)
    sessions = [Session(fp) for fp in session_files if compiled_pattern.match(str(fp))]
    
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

def get_session_file(profile_pattern: str=".*", session_pattern: str=".*") -> Path | None:
    profiles = _find_firefox_profiles(profile_pattern)
    profile_idx = get_user_choice([f"{p.path.name} | {p.session_number} sessions" for p in profiles], "profile")

    if profile_idx is None: return None
    selected_profile = profiles[profile_idx]

    sessions = _find_sessions(selected_profile.path, session_pattern)
    session_idx = get_user_choice([f"{s.path.name} ({_create_session_file_label(s.path)})" for s in sessions], "session")

    if session_idx is None: return None
    selected_session = sessions[session_idx]

    return selected_session.path

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Find and select Firefox profile and session.")
    parser.add_argument("--profile-regex", help="Regex to filter Firefox profiles", type=str, default=None)
    parser.add_argument("--session-regex", help="Regex to filter session files", type=str, default=None)
    args = parser.parse_args()

    session_file = get_session_file(profile_pattern=args.profile_regex, session_pattern=args.session_regex)
    if session_file:
        print(f"Session file path: {session_file}")
