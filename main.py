import datetime

import pathionista
import parsinista


def main():
    session_file = pathionista.get_session_file()
    session_data = parsinista.convert_and_save_session(session_file, generate_filename())


def generate_filename(postfix="firefox_session", extension="json"):
    # Get current timestamp in YYYYMMDD_HHMMSS format
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # Construct the filename
    filename = f"{timestamp}_{postfix}.{extension}"
    return filename


if __name__ == "__main__":
    main()
