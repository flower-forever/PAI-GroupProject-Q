from dataclasses import dataclass
from datetime import date
from .AttendanceStatus import AttendanceStatus

@dataclass
class AttendanceRecord:
    attendance_id: int
    student_id: str 
    session_date: date
    session_id: str
    status: AttendanceStatus

    def __post_init__(self):
        # Validate status type
        if not isinstance(self.status, AttendanceStatus):
            # Attempt to convert string to Enum class
            try:
                self.status = AttendanceStatus(self.status)
            except ValueError:
                raise ValueError(f"Invalid status: {self.status}")