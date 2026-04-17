import json
from pathlib import Path
from pydantic import BaseModel
from edu_agent.config import ToneType


class Student(BaseModel):
    id: str
    tone: ToneType


def load_students() -> list[Student]:
    raw_data = json.loads(Path("data/students.json").read_text(encoding="utf-8"))
    return [Student.model_validate(student) for student in raw_data]


def get_student(student_id: str) -> Student | None:
    return next((student for student in load_students() if student.id == student_id), None)
