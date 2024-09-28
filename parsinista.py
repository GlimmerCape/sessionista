import json
import lz4.block

MAGIC_NUMBER = b"mozLz40\0"  # it's not a number, but if you think about it hard enough it is


def decompress_session_file(file_path: str) -> dict:
    with open(file_path, "rb") as f:
        magic = f.read(8)
        if magic != MAGIC_NUMBER:
            raise ValueError("Invalid firefox sessionstore file format.")
        json_data = lz4.block.decompress(f.read())
        session = json.loads(json_data)
        return session


def simplify_session_data(session):
    simplified_data = []
    for window in session.get("windows", []):
        window_data = {"tabs": []}
        for tab in window.get("tabs", []):
            entries = []
            for entry in tab.get("entries", []):
                entries.append({"title": entry.get("title", ""), "url": entry.get("url", "")})
            window_data["tabs"].append(entries)
        simplified_data.append(window_data)
    return simplified_data


def save_simplified_session(simplified_data, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(simplified_data, f, ensure_ascii=False, indent=2)


def convert_and_save_session(input_file, output_file):
    decompressed = decompress_session_file(input_file)
    simplified = simplify_session_data(decompressed)
    save_simplified_session(simplified, output_file)


# def decompress_session_file(file_path):
#     with open(file_path, 'rb') as f:
#         magic = f.read(8)
#         if magic != b'mozLz40\x00':
#             raise ValueError("Not a valid mozlz4 file")
#         file_content = f.read()
#         return lz4.block.decompress(file_content)
