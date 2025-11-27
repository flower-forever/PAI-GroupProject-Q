import unittest
import sys
import os
import tempfile

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.auth_service import AuthService
from services.export_service import ExportService
from database.db_handler import DatabaseHandler

class TestAdvancedFeatures(unittest.TestCase):
    def setUp(self):
        self.test_db = "test_advanced_features.db"
        self.db = DatabaseHandler(self.test_db)
        self.auth = AuthService(self.test_db)
        self.export = ExportService(self.test_db)
        
        # Add test data
        self.student_id = self.db.add_student("Test Student", "test@university.com")
        self.db.record_attendance(self.student_id, 1, "CS101", "Present")
        self.db.add_wellbeing_survey(self.student_id, 1, 3, 7.0)
    
    def tearDown(self):
        self.db.close()
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def test_auth_login(self):
        """Test user authentication"""
        # Test successful login with default admin
        success = self.auth.login("admin", "admin123")
        self.assertTrue(success)
        self.assertIsNotNone(self.auth.current_user)
        
        # Test failed login
        success = self.auth.login("admin", "wrongpassword")
        self.assertFalse(success)
    
    def test_auth_permissions(self):
        """Test role-based permissions"""
        self.auth.login("admin", "admin123")
        self.assertTrue(self.auth.has_permission("admin"))
        self.assertTrue(self.auth.has_permission("officer"))
        self.assertTrue(self.auth.has_permission("director"))
        
        self.auth.login("wellbeing_officer", "officer123")
        self.assertFalse(self.auth.has_permission("admin"))
        self.assertTrue(self.auth.has_permission("officer"))
        self.assertTrue(self.auth.has_permission("director"))
    
    def test_export_students(self):
        """Test student data export"""
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp_file:
            filename = temp_file.name
        
        try:
            result_file = self.export.export_students_to_csv(filename)
            self.assertTrue(os.path.exists(result_file))
            self.assertGreater(os.path.getsize(result_file), 0)
        finally:
            if os.path.exists(filename):
                os.remove(filename)
    
    def test_comprehensive_report(self):
        """Test comprehensive report generation"""
        report = self.export.generate_comprehensive_report()
        self.assertIn('total_students', report)
        self.assertIn('average_stress_level', report)
        self.assertGreaterEqual(report['total_students'], 1)

if __name__ == '__main__':
    unittest.main()