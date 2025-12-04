from ast import If
from dataclasses import dataclass
from datetime import datetime
from re import I
from .AlertType import AlertType

@dataclass
class Alert:
    alert_id: int
    student_id: str
    alert_type: AlertType #changed it from str to AlertType
    reason: str
    created_at: datetime
    resolved: bool = False

    def __post_init__(self):
        # Ensure our alert_type is valid
        if not isinstance(self.alert_type, AlertType):
            try:
                self.alert_type = AlertType(self.alert_type)
            except ValueError:
                raise ValueError(f"Invalid alert type: {self.alert_type}")
        
    def mark_as_resolved(self):
        self.resolved = True