from dataclasses import dataclass
from datetime import date


@dataclass
class WellbeingRecord:
    record_id: int
    student_id: int
    week_start: date
    stress_level: int  # 1–5
    sleep_hours: float
    source_type: str = "survey"

    def __post_init__(self):
        # Data Validation Logic
        
        # Stress level must be between 1 and 5
        if not (1 <= self.stress_level <= 5):
            raise ValueError(f"Stress level must be between 1 and 5, got {self.stress_level}")

        # Sleep hours must be between 0 and 24
        if not (0 <= self.sleep_hours <= 24):
            raise ValueError(f"Sleep hours must be between 0 and 24, got {self.sleep_hours}")