"""Roster & Check-In module (Student A)."""
import json
from datetime import date, datetime
from pathlib import Path

LOG_FILE = Path("attendance_log.json")
VALID_STATUSES = {"Present", "Late"}


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


def add_student(name, student_id):
    """Create a student profile. Student IDs are stored in UPPERCASE and must be unique."""
    name = name.strip()
    student_id = student_id.strip().upper()
    if not name or not student_id:
        raise ValueError("Name and Student ID are both required.")

    data = load_log()
    if any(s["student_id"] == student_id for s in data["students"]):
        raise ValueError(f"Student ID {student_id} already exists.")

    student = {"student_id": student_id, "name": name}
    data["students"].append(student)
    save_log(data)
    return student
def check_in(student_id, status):
    """Log a timestamped Present/Late record for today.
    If the student already has a record today, update it instead of adding a second one.
    Returns (record, was_updated)."""
    student_id = student_id.strip().upper()
    status = status.strip().capitalize()
    if status not in VALID_STATUSES:
        raise ValueError("Status must be 'Present' or 'Late'.")

    data = load_log()
    if not any(s["student_id"] == student_id for s in data["students"]):
        raise ValueError(f"No student found with ID {student_id}.")

    today = date.today().isoformat()
    now = datetime.now().isoformat(timespec="seconds")

    for record in data["records"]:
        if record["student_id"] == student_id and record["date"] == today:
            record["status"] = status
            record["timestamp"] = now
            save_log(data)
            return record, True

    record = {"student_id": student_id, "date": today, "status": status, "timestamp": now}
    data["records"].append(record)
    save_log(data)
    return record, False