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