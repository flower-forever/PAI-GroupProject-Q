import unittest
import sys
import os
from datetime import date

# Path Configuration
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Imports 
from src.models.AttendanceRecord import AttendanceRecord
from src.models.AttendanceStatus import AttendanceStatus

class TestAttendanceRecord(unittest.TestCase):
    
    def setUp(self):
        # Setup a standard valid attendance record
        self.record = AttendanceRecord(
            attendance_id=1,
            student_id="u1234567", 
            session_date=date(2025, 11, 16),
            session_id="WM9QF",
            status=AttendanceStatus.PRESENT # Enum object
        )

    def test_initialization(self):
        # Test basic attribute storage
        self.assertEqual(self.record.attendance_id, 1)
        self.assertEqual(self.record.student_id, "u1234567")
        self.assertEqual(self.record.session_id, "WM9QF")
        self.assertEqual(self.record.status, AttendanceStatus.PRESENT)

    def test_status_str_behavior(self):
        # Test that status behaves like a string
        self.assertEqual(str(self.record.status), "PRESENT")
        self.assertEqual(f"Status is {self.record.status}", "Status is PRESENT")

    def test_status_string_conversion(self):
        # Test creating a record using a string for status instead of Enum object
        record_str_status = AttendanceRecord(
            attendance_id=2,
            student_id="u1234567",
            session_date=date(2025, 11, 16),
            session_id="WM9QF",
            status="ABSENT" # Passing string "ABSENT"
        )
        # It should automatically convert to the Enum type
        self.assertEqual(record_str_status.status, AttendanceStatus.ABSENT)
        self.assertIsInstance(record_str_status.status, AttendanceStatus)

    def test_invalid_status(self):
        # Test invalid status validation
        print("\nTesting invalid attendance status validation...")
        
        with self.assertRaisesRegex(ValueError, "Invalid status"):
            AttendanceRecord(
                attendance_id=3,
                student_id="u1234567",
                session_date=date(2025, 11, 16),
                session_id="WM9QF",
                status="SKIPPING" # Invalid status
            )
        print("-> Successfully blocked invalid status.")

if __name__ == '__main__':
    unittest.main()