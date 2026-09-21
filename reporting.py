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
