"""KAB Attendance Registry - main entry point."""
import roster
import reporting


def add_student_menu():
    name = input("Student name: ")
    student_id = input("Student ID: ")
    try:
        student = roster.add_student(name, student_id)
    except ValueError as err:
        print(err)
        return
    print(f"Added {student['name']} ({student['student_id']}).")


def check_in_menu():
    student_id = input("Student ID: ")
    status = input("Status (Present/Late): ")
    try:
        record, updated = roster.check_in(student_id, status)
    except ValueError as err:
        print(err)
        return
    action = "Updated" if updated else "Recorded"
    print(f"{action}: {record['student_id']} is {record['status']} at {record['timestamp']}.")


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
        print("1. Add student")
        print("2. Check in student (Present/Late)")
        print("3. Students checked in today")
        print("4. Mark absent students")
        print("5. Attendance rates")
        print("6. Absence streaks and chronically absent students")
        print("0. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_student_menu()
        elif choice == "2":
            check_in_menu()
        elif choice == "3":
            roster.print_checked_in_today()
        elif choice == "4":
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