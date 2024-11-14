import argparse
import datetime


import pathionista
from parsinista import Parsinista


def main():
    parser = argparse.ArgumentParser(description="CLI that remembers the last username and optionally takes output file path.")
    
    parser.add_argument(
        "-p","--profile", 
        type=bool, 
        help="The username of the user. If not provided, the last used username will be reused."
    )
    parser.add_argument(
        "-o","--output_file_path", 
        type=str,
        default=None,
        help="Output file path. Defaults to timestamp + postfix."
    )
    session_file_path = pathionista.get_session_file()
    if not session_file_path:
        print("No session file selected")
        return
    args = parser.parse_args()
    output_file_path = args.output_file_path
    if output_file_path == None:
        output_file_path = generate_filename()
    parser = Parsinista(session_file_path, output_file_path)
    session_data = parser.convert_and_save_session()


def generate_filename(postfix="firefox_session", extension="json"):
    # Get current timestamp in YYYYMMDD_HHMMSS format
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # Construct the filename
    filename = f"{timestamp}_{postfix}.{extension}"
    return filename


if __name__ == "__main__":
    main()
