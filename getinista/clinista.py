def get_user_choice(options: list[str], prompt: str) -> int | None:
    if not options:
        print(f"{prompt}. No options available to choose from")
        return None

    for i, option in enumerate(options, start=1):
        print(f"{i}: {option}")

    while True:
        try:
            choice = int(input(f"{prompt} (Enter the number or 0 to cancel): "))
            if choice == 0:
                print("Operation cancelled by the user.")
                return None
            if 1 <= choice <= len(options):
                return choice - 1
            else:
                print(f"Please enter a number between 1 and {len(options)}, or 0 to cancel.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

