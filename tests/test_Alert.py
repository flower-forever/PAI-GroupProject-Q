from re import S
import unittest
import os
import sys
from datetime import datetime

# Path configuration
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# import
from src.models.Alert import Alert
from src.models.AlertType import AlertType

class TestAlert(unittest.TestCase):
    def setUp(self):
        self.alert = Alert(
            alert_id=1,
            student_id="u12345",
            alert_type=AlertType.ATTENDANCE,
            reason="Missed 3 classes",
            created_at=datetime(2025, 12, 1)
        )

    def test_initialization(self):
        self.assertEqual(self.alert.student_id, "u12345")
        self.assertEqual(self.alert.alert_type, AlertType.ATTENDANCE)
        self.assertEqual(self.alert.reason, "Missed 3 classes")
        self.assertFalse(self.alert.resolved)  # Default resolved value should be False

    def test_alert_type_string_conversion(self):
        # Test creating an alert using a string for alert_type
        str_alert = Alert(
            alert_id=2,
            student_id="u1234567",
            alert_type="Wellbeing",  # Passing string
            reason="High stress level",
            created_at=datetime.now()
        )
        self.assertIsInstance(str_alert.alert_type, AlertType)
        self.assertEqual(str_alert.alert_type, AlertType.WELLBEING)

    def test_invalid_alert_type(self):
        # Test validation logic
        print("\nTesting invalid alert type...")
        with self.assertRaisesRegex(ValueError, "Invalid alert type"):
            Alert(
                alert_id=3,
                student_id="u1234567",
                alert_type="Drop out of school", # Invalid
                reason="Test",
                created_at=datetime.now()
            )
        print("-> Successfully blocked invalid alert type.")

    def test_mark_as_resolved(self):
        self.assertFalse(self.alert.resolved)
        self.alert.mark_as_resolved()
        self.assertTrue(self.alert.resolved)

if __name__ == '__main__':
    unittest.main()
