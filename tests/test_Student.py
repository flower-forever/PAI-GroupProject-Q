import unittest
import os
import sys

# import models
from src.models.Student import Student

# path configuration
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

class TestStudentModel(unittest.TestCase):
    
    def setUp(self):
        # setup test student instance #
        self.student = Student(
            student_id="s1234567",
            first_name="Harry",
            last_name="Potter",
            email="harry.potter@warwick.ac.uk",
            password="Harry_123",
            year=1
        )

    def test_initialization_and_attributes(self):
        # test student initialization and attributes #
        # verify all fields are correctly stored #
        self.assertEqual(self.student.student_id, "s1234567")
        self.assertEqual(self.student.first_name, "Harry")
        self.assertEqual(self.student.last_name, "Potter")
        self.assertEqual(self.student.email, "harry.potter@warwick.ac.uk")
        self.assertEqual(self.student.year, 1)

    def test_full_name_property(self):
        # test dynamic property #
        # verify full_name logic is correctly implemented #
        self.assertEqual(self.student.full_name, "Harry Potter")

    def test_update_attributes(self):
        # test attribute modification #
        # scenario: student promotion (Year 1 -> Year 2) or name change #
        self.student.year = 2
        self.assertEqual(self.student.year, 2)

        # modify last_name #
        self.student.last_name = "Weasley"
        # verify full_name is automatically updated #
        self.assertEqual(self.student.full_name, "Harry Weasley")

    def test_str_representation(self):
        # test string representation #
        # verify dataclass automatically generates string representation containing all fields #
        student_str = str(self.student)

        # verify output contains critical information #
        self.assertIn("s1234567", student_str)
        self.assertIn("Harry", student_str)
        self.assertIn("year=1", student_str)

    def test_datatype_validation_behavior(self):
        # test datatype validation behavior #
        with self.assertRaisesRegex(TypeError, "Year must be an integer"):
            Student(
                student_id="s001", 
                first_name="John", 
                last_name="Snow", 
                email="bad@email.com", 
                password="pass", 
                year="NotANumber"  # An incorrect type was passed in.
            )
        print("-> Year must be an integer")

        with self.assertRaisesRegex(ValueError, "Year must be a positive integer"):
            Student(
                student_id="s002", 
                first_name="John", 
                last_name="Snow",  
                email="bad@test.com", 
                password="pass", 
                year=-1  # Year should be positive
            )
            
        print("-> Year must be a positive integer")

        with self.assertRaisesRegex(ValueError, "Invalid email format"):
            Student(
                student_id="s003", 
                first_name="John", 
                last_name="Snow", 
                email="invalid_email_format", # Bad email format
                password="pass", 
                year=1
            )
        print("-> Invalid email format")

if __name__ == '__main__':
    unittest.main()