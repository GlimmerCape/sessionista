import argparse
import os
from datetime import datetime

def get_timestamped_filename(postfix="firefox"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{timestamp}_{postfix}.txt"

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
    parser.add_argument(
        "-r", "--reuse_last_user", 
        action="store_true", 
        help="Reuse the last saved username, overriding any provided username."
    )
    
    args = parser.parse_args()

if __name__ == "__main__":
    main()
