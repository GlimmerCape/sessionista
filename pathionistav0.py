import os
import platform
import sys

def get_firefox_profiles_dir():
    system = platform.system()
    home = os.path.expanduser("~")

    if system == "Windows":
        appdata = os.getenv('APPDATA')
        if not appdata:
            print("Unable to locate APPDATA directory.")
            sys.exit(1)
        profiles_dir = os.path.join(appdata, 'Mozilla', 'Firefox', 'Profiles')
    elif system == "Darwin":  # macOS
        profiles_dir = os.path.join(home, 'Library', 'Application Support', 'Firefox', 'Profiles')
    elif system == "Linux":
        profiles_dir = os.path.join(home, '.mozilla', 'firefox')
    else:
        # Check for WSL
        if 'microsoft' in platform.uname().release.lower():
            # Assuming WSL uses Linux paths
            profiles_dir = os.path.join(home, '.mozilla', 'firefox')
        else:
            print(f"Unsupported operating system: {system}")
            sys.exit(1)

    if not os.path.exists(profiles_dir):
        print(f"Firefox profiles directory not found at: {profiles_dir}")
        sys.exit(1)

    return profiles_dir

def list_profiles(profiles_dir):
    profiles = []
    for entry in os.listdir(profiles_dir):
        full_path = os.path.join(profiles_dir, entry)
        if os.path.isdir(full_path) and entry.endswith(".default") or entry.endswith(".default-release"):
            profiles.append(entry)
    if not profiles:
        # If no profiles with .default or .default-release, list all directories
        profiles = [entry for entry in os.listdir(profiles_dir) if os.path.isdir(os.path.join(profiles_dir, entry))]
    
    return profiles

def prompt_profile_selection(profiles):
    if not profiles:
        print("No Firefox profiles found.")
        sys.exit(1)
    elif len(profiles) == 1:
        print(f"Only one profile found: {profiles[0]}")
        return profiles[0]
    else:
        print("Multiple Firefox profiles found:")
        for idx, profile in enumerate(profiles, start=1):
            print(f"{idx}. {profile}")
        while True:
            try:
                choice = int(input(f"Select a profile (1-{len(profiles)}): "))
                if 1 <= choice <= len(profiles):
                    return profiles[choice - 1]
                else:
                    print(f"Please enter a number between 1 and {len(profiles)}.")
            except ValueError:
                print("Invalid input. Please enter a number.")

def find_session_file(profile_path):
    # Common session file names in Firefox
    session_files = [
        "sessionstore.jsonlz4",
        "recovery.jsonlz4",
        "previous.jsonlz4"
    ]
    for filename in session_files:
        file_path = os.path.join(profile_path, filename)
        if os.path.exists(file_path):
            return file_path
    # Sometimes session data might be in a folder like "sessionstore-backups"
    backup_dir = os.path.join(profile_path, "sessionstore-backups")
    if os.path.exists(backup_dir):
        for filename in session_files:
            file_path = os.path.join(backup_dir, filename)
            if os.path.exists(file_path):
                return file_path
    return None

def get_session_file():
    print("Firefox Session File Locator")
    print("============================\n")
    
    profiles_dir = get_firefox_profiles_dir()
    profiles = list_profiles(profiles_dir)
    selected_profile = prompt_profile_selection(profiles)
    profile_path = os.path.join(profiles_dir, selected_profile)
    
    session_file = find_session_file(profile_path)
    if session_file:
        print(f"\nSession file found at:\n{session_file}")
    else:
        print("\nNo session file found in the selected profile.")
    return session_file
