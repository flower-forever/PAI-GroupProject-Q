import unittest
import sys
import os
from datetime import date
from src.models.WellbeingRecord import WellbeingRecord

# --- path configuration ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

class TestWellbeingRecord(unittest.TestCase):
    
    def setUp(self):
        # Prepare a valid record
        self.record = WellbeingRecord(
            record_id=1,
            student_id=101,
            week_start=date(2025, 12, 1),
            stress_level=3,      
            sleep_hours=7.5,     
            # source_type
        )

    def test_initialization(self):
        # Test basic field storage
        self.assertEqual(self.record.stress_level, 3)
        self.assertEqual(self.record.sleep_hours, 7.5)
        self.assertEqual(self.record.week_start, date(2025, 12, 1))

    def test_default_values(self):
        # Test default parameters
        # We didn't pass source_type in setUp, it should default to "survey".
        self.assertEqual(self.record.source_type, "survey")

    def test_custom_source_type(self):
        # Test coverage default value
        manual_record = WellbeingRecord(
            record_id=2, student_id=202, week_start=date(2025, 12, 1),
            stress_level=4, sleep_hours=8,
            source_type="interview"
        )
        self.assertEqual(manual_record.record_id, 2)
        self.assertEqual(manual_record.student_id, 202)
        self.assertEqual(manual_record.week_start, date(2025, 12, 1))
        self.assertEqual(manual_record.stress_level, 4)
        self.assertEqual(manual_record.sleep_hours, 8)
        self.assertEqual(manual_record.source_type, "interview")

    def test_validation_stress_level(self):
        # Test stress level range validation (1-5)
    
        # stress level is 0
        with self.assertRaisesRegex(ValueError, "Stress level must be between 1 and 5"):
            WellbeingRecord(
                record_id=3, student_id=101, week_start=date(2025, 12, 1),
                stress_level=0,  # Error
                sleep_hours=8
            )
            
        # Stress level is too high
        with self.assertRaisesRegex(ValueError, "Stress level must be between 1 and 5"):
            WellbeingRecord(
                record_id=3, student_id=101, week_start=date(2025, 12, 1),
                stress_level=6,  # Error
                sleep_hours=8
            )
        print("-> stress level passed")

    def test_validation_sleep_hours(self):
        # Test reasonableness of sleep time (0-24)
        
        # Negative sleep hours
        with self.assertRaisesRegex(ValueError, "Sleep hours must be between 0 and 24"):
            WellbeingRecord(
                record_id=4, student_id=101, week_start=date(2024, 11, 1),
                stress_level=3,
                sleep_hours=-1.5 # Error
            )
            
        # Over 24 hours
        with self.assertRaisesRegex(ValueError, "Sleep hours must be between 0 and 24"):
            WellbeingRecord(
                record_id=4, student_id=101, week_start=date(2024, 11, 1),
                stress_level=3,
                sleep_hours=25 # Error
            )
        print("-> Sleep time boundary validation passed.")

if __name__ == '__main__':
    unittest.main()