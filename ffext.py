import os
import json
import lz4.block
from datetime import datetime

def is_wsl():
    # Check if the script is running under WSL
    return 'microsoft' in os.uname().release.lower()

def get_firefox_profiles(windows_username=None):
    profiles = []
    if os.name == 'nt':
        # Windows path
        appdata = os.getenv('APPDATA')
        session_path = os.path.join(appdata, 'Mozilla', 'Firefox', 'Profiles')
    elif is_wsl():
        # WSL path - access the Windows file system
        if not windows_username:
            windows_username = input("Enter your Windows username: ")
        wsl_root = '/mnt/c'
        appdata = os.path.join(wsl_root, 'Users', windows_username, 'AppData', 'Roaming')
        session_path = os.path.join(appdata, 'Mozilla', 'Firefox', 'Profiles')
    else:
        # Unix/Linux/Mac path
        home = os.getenv('HOME')
        session_path = os.path.join(home, '.mozilla', 'firefox')

    if os.path.exists(session_path):
        for profile in os.listdir(session_path):
            if profile.endswith('.default') or profile.endswith('.default-release'):
                profiles.append(profile)
    return profiles, session_path

def find_firefox_session_files(session_path, profile):
    profile_path = os.path.join(session_path, profile)
    session_folder = os.path.join(profile_path, 'sessionstore-backups')
    session_files = []
    
    if os.path.isdir(session_folder):
        for file_name in os.listdir(session_folder):
            if '.jsonlz4' in file_name:
                file_path = os.path.join(session_folder, file_name)
                timestamp = os.path.getmtime(file_path)
                session_files.append((file_path, timestamp))
    
    return session_files

def choose_session_file(session_files):
    print("Available session files:")
    for i, (session_file, timestamp) in enumerate(session_files):
        formatted_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        print(f"{i + 1}: {session_file} (Last modified: {formatted_time})")
    
    choice = int(input("Choose a session file (enter the number): ")) - 1
    if 0 <= choice < len(session_files):
        return session_files[choice][0]  # Return the file path
    else:
        print("Invalid choice")
        exit(1)

def decompress_lz4(file_path):
    with open(file_path, 'rb') as f:
        # Read the file and decompress it
        magic = f.read(8)
        if magic != b'mozLz40\x00':
            raise ValueError("Not a valid mozlz4 file")
        file_content = f.read()
        return lz4.block.decompress(file_content)

def parse_session_file(session_file):
    session_data = decompress_lz4(session_file)
    return json.loads(session_data)

def save_session_info(session_data, output_file):
    session_info = []
    
    # Process open windows and tabs
    for window in session_data['windows']:
        window_info = {"tabs": []}
        for tab in window['tabs']:
            tab_info = {"entries": []}
            for entry in tab['entries']:
                tab_info["entries"].append({"title": entry['title'], "url": entry['url']})
            window_info["tabs"].append(tab_info)
        session_info.append(window_info)

    # Process closed windows and tabs
    if 'closed_windows' in session_data:
        for closed_window in session_data['closed_windows']:
            closed_window_info = {"tabs": []}
            for tab in closed_window['tabs']:
                tab_info = {"entries": []}
                for entry in tab['entries']:
                    tab_info["entries"].append({"title": entry['title'], "url": entry['url']})
                closed_window_info["tabs"].append(tab_info)
            session_info.append(closed_window_info)
    
    # Save the session_info to the output_file (not shown here)
    with open(output_file, 'w') as f:
        json.dump(session_data, f, indent=2)

def choose_profile(profiles):
    print("Available profiles:")
    for i, profile in enumerate(profiles):
        print(f"{i + 1}: {profile}")
    
    choice = int(input("Choose a profile (enter the number): ")) - 1
    if 0 <= choice < len(profiles):
        return profiles[choice]
    else:
        print("Invalid choice")
        exit(1)

if __name__ == '__main__':
    profiles, session_path = get_firefox_profiles()
    if profiles:
        profile = choose_profile(profiles)
        session_files = find_firefox_session_files(session_path, profile)
        if session_files:
            session_file = choose_session_file(session_files)
            timestamp = datetime.now().strftime('%d-%m-%Y')
            session_data = parse_session_file(session_file)
            output_file = f'ff_sesh_{timestamp}.json'
            save_session_info(session_data, output_file)
            print(f"Session info saved to {output_file}")
        else:
            print(f"No session file found for profile {profile}.")
    else:
        print("No Firefox profiles found.")
