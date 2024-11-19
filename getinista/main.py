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
        type=bool,
        default=False,
        help="By default cli adds '.*' at the beginning and end of the patterns"
    )
    parser.add_argument(
        "-o","--output-file-path", 
        type=str,
        default=None,
        help="Output file path. Defaults to timestamp + postfix."
    )
    args = parser.parse_args()
    profile_pattern = args.profile_pattern if args.raw_patterns else add_wildcards_to_pattern(args.profile_pattern)
    session_pattern = args.session_pattern if args.raw_patterns else add_wildcards_to_pattern(args.session_pattern)

    session_file_path = pathionista.get_session_file(profile_pattern=profile_pattern, session_pattern=session_pattern)
    if not session_file_path:
        print("No session file selected")
        return

    output_file_path = args.output_file_path
    if output_file_path == None:
        output_file_path = generate_filename()

    parser = Parsinista(session_file_path, output_file_path)
    parser.convert_and_save_session()


def generate_filename(postfix="firefox_session", extension="json"):
    # Get current timestamp in YYYYMMDD_HHMMSS format
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # Construct the filename
    filename = f"{timestamp}_{postfix}.{extension}"
    return filename

def add_wildcards_to_pattern(pattern: str) -> str:
    return PYTHON_WILDCARD + pattern + PYTHON_WILDCARD    

if __name__ == "__main__":
    main()
