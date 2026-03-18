def get_positive_int(prompt: str) -> int:
    """Ask the user for a positive integer; repeat until a valid value is entered."""
    while True:
        try:
            n = int(input(prompt))
            if n > 0:
                return n
            print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter an integer.")


def print_pyramid(n: int) -> None:
    """Centered pyramid of numbers 1…row."""
    for i in range(1, n + 1):
        # leading spaces to centre the row
        spaces = " " * (n - i)
        nums = " ".join(str(j) for j in range(1, i + 1))
        print(f"{spaces}{nums}")


def print_diamond(n: int) -> None:
    """Diamond made from a pyramid and its inverted copy."""
    print_pyramid(n)
    for i in range(n - 1, 0, -1):
        spaces = " " * (n - i)
        nums = " ".join(str(j) for j in range(1, i + 1))
        print(f"{spaces}{nums}")


def print_number_triangle(n: int) -> None:
    """Triangle with a running counter, 1 number on first row, 2 on second, …"""
    num = 1
    for i in range(1, n + 1):
        row = " ".join(str(num + j) for j in range(i))
        print(row)
        num += i


def main() -> None:
    while True:
        print("\nNumber Pattern Generator")
        print("1. Pyramid")
        print("2. Diamond")
        print("3. Number triangle")
        choice = input("Choose a pattern (1–3): ").strip()
        if choice not in ("1", "2", "3"):
            print("Invalid choice; please select 1, 2 or 3.")
            continue

        size = get_positive_int("Enter pattern size (positive integer): ")

        if choice == "1":
            print_pyramid(size)
        elif choice == "2":
            print_diamond(size)
        else:  # choice == "3"
            print_number_triangle(size)

        again = input("Generate another pattern? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()