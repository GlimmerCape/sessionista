import argparse
import datetime

import pathionista
from parsinista import Parsinista

PYTHON_WILDCARD = ".*"

def main():
    parser = argparse.ArgumentParser(description="CLI tool for getting and saving firefox session files.")
    
    parser.add_argument(
        "-p","--profile-pattern", 
        type=str, 
        default=".*",
        help="Profiles will be filtered by this pattern using python regex",
    )
    parser.add_argument(
        "-s","--session-pattern", 
        type=str, 
        default=".*",
        help="Session files will be filtered by this pattern using python regex",
    )
    parser.add_argument(
        "-r", "--raw-patterns",
        action="store_true",
        help="By default cli adds '.*' at the beginning and end of the patterns"
    )
    parser.add_argument(
        "-o","--output-file-path", 
        type=str,
        default=None,
        help="Output file path. Defaults to timestamp + postfix."
    )
    parser.add_argument(
        "--pick-windows-to-save",
        action="store_true",
        help="Whether to ask the user to pick windows to be saved"
    )
    args = parser.parse_args()

    session_file_path = pathionista.get_session_file(args.profile_pattern, args.session_pattern, args.raw_patterns)
    if not session_file_path:
        print("No session file selected")
        return

    output_file_path = args.output_file_path
    if output_file_path == None:
        output_file_path = generate_filename()

    parser = Parsinista(session_file_path, output_file_path)
    parser.convert_and_save_session(args.pick_windows_to_save)


def generate_filename(postfix="firefox_session", extension="json"):
    # Get current timestamp in YYYYMMDD_HHMMSS format
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # Construct the filename
    filename = f"{timestamp}_{postfix}.{extension}"
    return filename

if __name__ == "__main__":
    main()
