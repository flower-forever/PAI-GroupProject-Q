import unittest
import sys
import os
import tempfile

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from database.db_handler import DatabaseHandler
from services.analytics_service import AnalyticsService
from services.auth_service import AuthService
from services.export_service import ExportService
from cli_interface import CLIInterface

class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system"""
    
    def setUp(self):
        self.test_db = "test_integration.db"
        self.db = DatabaseHandler(self.test_db)
        self.analytics = AnalyticsService(self.test_db)
        self.auth = AuthService(self.test_db)
        self.export = ExportService(self.test_db)
        
        # Create test data
        self.student_id = self.db.add_student("Integration Test", "integration@test.com")
        self.db.record_attendance(self.student_id, 1, "CS101", "Present")
        self.db.add_wellbeing_survey(self.student_id, 1, 3, 7.5, "Test survey")
        self.db.add_coursework(self.student_id, "CS101", "Test Assignment", "2024-01-15", "Submitted", 85.0)
    
    def tearDown(self):
        self.db.close()
        self.analytics.close()
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def test_end_to_end_student_workflow(self):
        """Test complete student workflow"""
        # Add student
        student_id = self.db.add_student("End-to-End Test", "e2e@test.com")
        self.assertGreater(student_id, 0)
        
        # Record attendance
        attendance_id = self.db.record_attendance(student_id, 1, "CS101", "Present")
        self.assertGreater(attendance_id, 0)
        
        # Add wellbeing survey
        survey_id = self.db.add_wellbeing_survey(student_id, 1, 2, 8.0, "Good")
        self.assertGreater(survey_id, 0)
        
        # Generate analytics
        attendance_rate = self.analytics.calculate_average_attendance(student_id)
        self.assertEqual(attendance_rate, 100.0)
        
        # Export data
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp_file:
            filename = temp_file.name
        
        try:
            result_file = self.export.export_students_to_csv(filename)
            self.assertTrue(os.path.exists(result_file))
        finally:
            if os.path.exists(filename):
                os.remove(filename)
    
    def test_authentication_integration(self):
        """Test authentication integration"""
        # Login
        success = self.auth.login("admin", "admin123")
        self.assertTrue(success)
        self.assertIsNotNone(self.auth.current_user)
        
        # Check permissions
        self.assertTrue(self.auth.has_permission("admin"))
        self.assertTrue(self.auth.has_permission("officer"))
        
        # Logout
        self.auth.logout()
        self.assertIsNone(self.auth.current_user)
    
    def test_analytics_integration(self):
        """Test analytics integration with database"""
        # Get performance summary
        summary = self.analytics.get_student_performance_summary(self.student_id)
        self.assertIn('attendance_rate', summary)
        self.assertIn('average_stress', summary)
        self.assertIn('average_grade', summary)
        
        # Get stress trends
        trends = self.analytics.get_stress_trends(self.student_id)
        self.assertEqual(len(trends), 1)
        self.assertEqual(trends[0]['stress_level'], 3)
        
        # Identify high stress
        high_stress = self.analytics.identify_high_stress_weeks(self.student_id, threshold=2)
        self.assertEqual(len(high_stress), 1)
    
    def test_cli_interface_creation(self):
        """Test CLI interface can be created and has required methods"""
        cli = CLIInterface()
        
        # Check required methods exist
        self.assertTrue(hasattr(cli, 'display_main_menu'))
        self.assertTrue(hasattr(cli, 'run'))
        self.assertTrue(hasattr(cli, 'student_management_menu'))
        
        cli.db.close()
        cli.analytics.close()

if __name__ == '__main__':
    unittest.main()