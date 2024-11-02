import argparse
import datetime


import pathionista
import parsinista


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
    session_file = pathionista.get_session_file()
    args = parser.parse_args()
    file_path = args.output_file_path
    if file_path == None:
        file_path = generate_filename()
    session_data = parsinista.convert_and_save_session(session_file, file_path)


def generate_filename(postfix="firefox_session", extension="json"):
    # Get current timestamp in YYYYMMDD_HHMMSS format
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # Construct the filename
    filename = f"{timestamp}_{postfix}.{extension}"
    return filename


if __name__ == "__main__":
    main()
