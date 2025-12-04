import unittest
import sys
import os
from datetime import datetime

# Path Configuration
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Imports
from src.models.AuditLog import AuditLog
from src.models.ActionType import ActionType

class TestAuditLog(unittest.TestCase):
    
    def setUp(self):
        self.log = AuditLog(
            log_id=1001,
            user_id="u_admin_01",
            entity_type="Admin",
            entity_id="admin123",
            action_type=ActionType.UPDATE,
            timestamp=datetime.now(),
            details="Updated student information"
        )

    def test_initialization(self):
        self.assertEqual(self.log.user_id, "u_admin_01")
        self.assertEqual(self.log.entity_type, "Admin")
        self.assertEqual(self.log.action_type, ActionType.UPDATE)
        self.assertEqual(self.log.entity_id, "admin123")
        self.assertEqual(self.log.details, "Updated student information")

    def test_default_details(self):
        # Test the default value of the details field is an empty string
        simple_log = AuditLog(
            log_id=1002,
            user_id="u_officer_02",
            entity_type="Alert",
            entity_id="99",
            action_type=ActionType.CREATE,
            timestamp=datetime.now()
            # details default
        )
        self.assertEqual(simple_log.details, "")

    def test_action_type_string_conversion(self):
        # Test automatic conversion of string to enum object
        log_from_str = AuditLog(
            log_id=1003,
            user_id="u_test_03",
            entity_type="User",
            entity_id="u_new",
            action_type="LOGIN", # pass string
            timestamp=datetime.now()
        )
        self.assertEqual(log_from_str.action_type, ActionType.LOGIN)
        self.assertIsInstance(log_from_str.action_type, ActionType)

    def test_invalid_action_type(self):
        # Test illegal action type
        with self.assertRaisesRegex(ValueError, "Invalid action_type"):
            AuditLog(
                log_id=1004,
                user_id="u_check_04",
                entity_type="Student",
                entity_id="33945",
                action_type="DESTROY_DATABASE", # Invalid action_type
                timestamp=datetime.now()
            )

if __name__ == '__main__':
    unittest.main()