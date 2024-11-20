from typing import Callable

def ask_for_valid_input(prompt: str, validate_func: Callable[[str], bool]) -> str:
    while True:
        user_input = input(prompt)
        if validate_func(user_input):
            return user_input

def get_user_choice(options: list[str], item_name: str) -> int | None:
    if not options:
        print(f"Not a single {item_name} to choose from")
        return None

    if len(options) ==1:
        print(f"Single {item_name} in options list. Option chosen automatically: {options[0]}")
        return 0

    print(f"\nSelect a/an {item_name}")
    for i, option in enumerate(options, start=1):
        print(f"{i}: {option}")

    def validate_choice_from_list(value: str) -> bool:
        try:
            choice = int(value)
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return False
        if choice < 0 or len(options) < choice:
            print(f"Please enter a number between 1 and {len(options)}, or 0 to cancel.")
            return False
        return True

    choice = int(ask_for_valid_input("Enter the number or 0 to cancel: ", validate_choice_from_list))

    if choice == 0:
        print("Operation cancelled by the user.")
        return None
    return choice - 1

