import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.analytics_service import AnalyticsService
from database.db_handler import DatabaseHandler

class TestAnalyticsService(unittest.TestCase):
    def setUp(self):
        self.test_db = "test_analytics.db"
        self.db = DatabaseHandler(self.test_db)
        self.analytics = AnalyticsService(self.test_db)
        
        # Add test data
        self.student_id = self.db.add_student("Analytics Test", "analytics@test.com")
        self.db.record_attendance(self.student_id, 1, "CS101", "Present")
        self.db.record_attendance(self.student_id, 2, "CS101", "Absent")
        self.db.add_wellbeing_survey(self.student_id, 1, 2, 7.5)
        self.db.add_wellbeing_survey(self.student_id, 2, 4, 5.0)
        self.db.add_coursework(self.student_id, "CS101", "Test Assignment", "2024-01-15", "Submitted", 85.0)
    
    def tearDown(self):
        self.db.close()
        self.analytics.close()
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def test_calculate_average_attendance(self):
        attendance = self.analytics.calculate_average_attendance(self.student_id)
        self.assertEqual(attendance, 50.0)  # 1 present out of 2 classes
    
    def test_get_stress_trends(self):
        trends = self.analytics.get_stress_trends(self.student_id)
        self.assertEqual(len(trends), 2)
        self.assertEqual(trends[0]['stress_level'], 2)
    
    def test_identify_high_stress_weeks(self):
        high_stress = self.analytics.identify_high_stress_weeks(self.student_id, threshold=3)
        self.assertEqual(len(high_stress), 1)
        self.assertEqual(high_stress[0]['stress_level'], 4)
    
    def test_get_student_performance_summary(self):
        summary = self.analytics.get_student_performance_summary(self.student_id)
        self.assertIn('attendance_rate', summary)
        self.assertIn('average_stress', summary)
        self.assertIn('average_grade', summary)

if __name__ == '__main__':
    unittest.main()