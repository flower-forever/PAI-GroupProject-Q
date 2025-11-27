import unittest
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from database.db_handler import DatabaseHandler

class TestDatabase(unittest.TestCase):
    def setUp(self):
        """Set up a test database before each test"""
        self.test_db = "test_student_wellbeing.db"
        self.db_handler = DatabaseHandler(self.test_db)
    
    def tearDown(self):
        """Clean up after each test"""
        if self.db_handler.connection:
            self.db_handler.close()
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def test_database_connection(self):
        """Test that database connection works"""
        self.assertIsNotNone(self.db_handler.connection)
        self.assertTrue(self.db_handler.connection)
    
    def test_tables_created(self):
        """Test that all tables are created"""
        cursor = self.db_handler.connection.cursor()
        
        # Check students table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='students'")
        self.assertIsNotNone(cursor.fetchone())
        
        # Check attendance table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='attendance'")
        self.assertIsNotNone(cursor.fetchone())
    
    def test_add_student(self):
        """Test adding a new student"""
        student_id = self.db_handler.add_student("John Doe", "john@university.com")
        self.assertGreater(student_id, 0)
    
    def test_get_all_students(self):
        """Test retrieving all students"""
        # Add a test student first
        self.db_handler.add_student("Jane Smith", "jane@university.com")
        
        students = self.db_handler.get_all_students()
        self.assertEqual(len(students), 1)
        self.assertEqual(students[0]['name'], "Jane Smith")
    
    def test_get_student_by_id(self):
        """Test retrieving a specific student by ID"""
        student_id = self.db_handler.add_student("Test Student", "test@university.com")
        
        student = self.db_handler.get_student_by_id(student_id)
        self.assertIsNotNone(student)
        self.assertEqual(student['name'], "Test Student")
    
    def test_record_attendance(self):
        """Test recording attendance"""
        student_id = self.db_handler.add_student("Attendance Test", "attendance@test.com")
        attendance_id = self.db_handler.record_attendance(student_id, 1, "CS101", "Present")
        self.assertGreater(attendance_id, 0)
    
    def test_add_wellbeing_survey(self):
        """Test adding wellbeing survey"""
        student_id = self.db_handler.add_student("Survey Test", "survey@test.com")
        survey_id = self.db_handler.add_wellbeing_survey(student_id, 1, 3, 7.5, "Feeling okay")
        self.assertGreater(survey_id, 0)
    
    def test_add_coursework(self):
        """Test adding coursework"""
        student_id = self.db_handler.add_student("Coursework Test", "coursework@test.com")
        coursework_id = self.db_handler.add_coursework(student_id, "CS101", "Assignment 1", "2024-01-15", "Submitted", 85.5)
        self.assertGreater(coursework_id, 0)
    
    def test_update_student(self):
        """Test updating student information"""
        student_id = self.db_handler.add_student("Update Test", "update@test.com")
        
        # Update name only
        success = self.db_handler.update_student(student_id, name="Updated Name")
        self.assertTrue(success)
        
        student = self.db_handler.get_student_by_id(student_id)
        self.assertEqual(student['name'], "Updated Name")
    
    def test_delete_student(self):
        """Test deleting a student"""
        student_id = self.db_handler.add_student("Delete Test", "delete@test.com")
        
        # Add some related records
        self.db_handler.record_attendance(student_id, 1, "TEST101", "Present")
        self.db_handler.add_wellbeing_survey(student_id, 1, 3, 7.0)
        
        # Delete student
        success = self.db_handler.delete_student(student_id)
        self.assertTrue(success)
        
        # Verify student is gone
        student = self.db_handler.get_student_by_id(student_id)
        self.assertIsNone(student)
    
    def test_search_students(self):
        """Test student search functionality"""
        self.db_handler.add_student("John Smith", "john@test.com")
        self.db_handler.add_student("Jane Smith", "jane@test.com")
        self.db_handler.add_student("Bob Wilson", "bob@test.com")
        
        # Search by name
        results = self.db_handler.search_students("Smith")
        self.assertEqual(len(results), 2)
        
        # Search by email
        results = self.db_handler.search_students("john")
        self.assertEqual(len(results), 1)

if __name__ == '__main__':
    unittest.main()