"""Absence & Reporting module (Student B)."""
import json
from datetime import date, datetime
from pathlib import Path

LOG_FILE = Path("attendance_log.json")
ATTENDED = {"Present", "Late"}
CHRONIC_THRESHOLD = 85.0


def load_log():
    """Read attendance_log.json; return an empty structure if missing or broken."""
    if not LOG_FILE.exists():
        return {"students": [], "records": []}
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return {"students": [], "records": []}
    data.setdefault("students", [])
    data.setdefault("records", [])
    return data


def save_log(data):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_school_days(data):
    """A school day is any date that has at least one record."""
    return sorted({r["date"] for r in data["records"]})


def get_status(data, student_id, day):
    """Status of a student on a day. No record counts as Absent."""
    for r in data["records"]:
        if r["student_id"] == student_id and r["date"] == day:
            return r["status"]
    return "Absent"


def mark_absent(day=None):
    """Flag every student with no record on `day` as Absent. Returns flagged students."""
    day = day or date.today().isoformat()
    try:
        datetime.strptime(day, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format.")

    data = load_log()
    recorded = {r["student_id"] for r in data["records"] if r["date"] == day}
    flagged = []
    for student in data["students"]:
        if student["student_id"] not in recorded:
            data["records"].append({
                "student_id": student["student_id"],
                "date": day,
                "status": "Absent",
                "timestamp": datetime.now().isoformat(timespec="seconds"),
            })
            flagged.append(student)
    save_log(data)
    return flagged


def attendance_rate(data, student_id):
    """(days present or late) / (total school days) * 100."""
    days = get_school_days(data)
    if not days:
        return 0.0
    attended = sum(1 for d in days if get_status(data, student_id, d) in ATTENDED)
    return round(attended / len(days) * 100, 1)


def chronically_absent(data, threshold=CHRONIC_THRESHOLD):
    """Students below the threshold, lowest rate first."""
    if not get_school_days(data):
        return []
    result = []
    for s in data["students"]:
        rate = attendance_rate(data, s["student_id"])
        if rate < threshold:
            result.append((s, rate))
    return sorted(result, key=lambda item: item[1])


def find_absence_streaks(data, min_length=3):
    """Find runs of consecutive absent school days of at least min_length."""
    days = get_school_days(data)
    streaks = []
    for s in data["students"]:
        run = []
        for d in days + [None]:  # None marks the end so the last run is checked
            if d is not None and get_status(data, s["student_id"], d) == "Absent":
                run.append(d)
            else:
                if len(run) >= min_length:
                    streaks.append((s, run[0], run[-1], len(run)))
                run = []
    return sorted(streaks, key=lambda x: x[3], reverse=True)


def print_rates():
    data = load_log()
    days = get_school_days(data)
    print(f"\nAttendance rates ({len(days)} school days recorded)")
    print("-" * 40)
    if not data["students"]:
        print("No students found.")
        return
    for s in data["students"]:
        rate = attendance_rate(data, s["student_id"])
        print(f"{s['student_id']:<8}{s['name']:<20}{rate:>6.1f}%")


def print_streaks(min_length=3):
    data = load_log()
    streaks = find_absence_streaks(data, min_length)
    print(f"\nAbsence streaks ({min_length}+ school days in a row)")
    print("-" * 40)
    if not streaks:
        print("No streaks found.")
        return
    for s, start, end, length in streaks:
        print(f"{s['student_id']:<8}{s['name']:<15}{length} days ({start} to {end})")


def print_chronic():
    data = load_log()
    rows = chronically_absent(data)
    print(f"\nChronically absent students (below {CHRONIC_THRESHOLD:.0f}%)")
    print("-" * 40)
    if not rows:
        print("None. Everyone is at or above the threshold.")
        return
    for s, rate in rows:
        print(f"{s['student_id']:<8}{s['name']:<20}{rate:>6.1f}%")
