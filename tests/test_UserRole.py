import unittest
import os
import sys

# import models
from src.models.UserRole import UserRole

# path configuration
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

class TestUserRole(unittest.TestCase):
    # test role values #
    def test_role_values(self):
        # test enum values #
        self.assertEqual(UserRole.ADMIN, "ADMIN")
        self.assertEqual(UserRole.STUDENT, "STUDENT")
        self.assertEqual(UserRole.WELLBEING_OFFICER, "WELLBEING_OFFICER")
        self.assertEqual(UserRole.COURSE_DIRECTOR, "COURSE_DIRECTOR")

    def test_str_behavior(self):
        # test enum can be used as a string #
        self.assertTrue(UserRole.ADMIN == "ADMIN")
        
        # test f-string behavior #
        role_info = f"Role is {UserRole.STUDENT}"
        self.assertEqual(role_info, "Role is STUDENT")

    def test_enum_iteration(self):
        # test enum iteration #
        roles = list(UserRole)
        self.assertEqual(len(roles), 4)
        self.assertIn(UserRole.ADMIN, roles)
        self.assertIn(UserRole.WELLBEING_OFFICER, roles)

    def test_invalid_role(self):
        # test invalid role #
        with self.assertRaises(ValueError):
            UserRole("SUPER_HACKER")
        print("warning: you created an invalid role")
        
if __name__ == '__main__':
    unittest.main()