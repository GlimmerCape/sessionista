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

    while True:
        try:
            choice = int(input(f"Enter the number or 0 to cancel: "))
            if choice == 0:
                print("Operation cancelled by the user.")
                return None
            if 1 <= choice <= len(options):
                return choice - 1
            else:
                print(
                    f"Please enter a number between 1 and {len(options)}, or 0 to cancel."
                )
        except ValueError:
            print("Invalid input. Please enter a valid number.")
