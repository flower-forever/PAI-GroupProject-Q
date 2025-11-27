import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.student import Student

class TestModels(unittest.TestCase):
    def test_student_creation(self):
        student = Student(1, "John Doe", "john@university.com")
        self.assertEqual(student.name, "John Doe")

if __name__ == '__main__':
    unittest.main()
    