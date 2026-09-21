"""KAB Attendance Registry - main entry point."""
import reporting


def mark_absent_menu():
    day = input("Date (YYYY-MM-DD, blank for today): ").strip() or None
    try:
        flagged = reporting.mark_absent(day)
    except ValueError as err:
        print(err)
        return
    if flagged:
        print("Marked Absent: " + ", ".join(s["name"] for s in flagged))
    else:
        print("No missing students. Everyone already has a record.")


def main():
    while True:
        print("\n=== KAB Attendance Registry ===")
        # Roster options (1-3) are added by Student A
        print("4. Mark absent students")
        print("5. Attendance rates")
        print("6. Absence streaks and chronically absent students")
        print("0. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "4":
            mark_absent_menu()
        elif choice == "5":
            reporting.print_rates()
        elif choice == "6":
            reporting.print_streaks()
            reporting.print_chronic()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
