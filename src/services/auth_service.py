import hashlib
import secrets
from typing import Dict, Optional

class AuthService:
    def __init__(self, db_path: str = "student_wellbeing.db"):
        self.db_path = db_path
        self.current_user = None
        self._create_users_table()
    
    def _create_users_table(self):
        """Create users table if it doesn't exist"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'officer', 'director')),
                full_name TEXT NOT NULL,
                created_date DATE DEFAULT CURRENT_DATE
            )
        ''')
        
        # Create default admin user if no users exist
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            self._create_default_users(cursor)
        
        conn.commit()
        conn.close()
    
    def _create_default_users(self, cursor):
        """Create default users for the system"""
        default_users = [
            ('admin', 'admin123', 'admin', 'System Administrator'),
            ('wellbeing_officer', 'officer123', 'officer', 'Student Wellbeing Officer'),
            ('course_director', 'director123', 'director', 'Course Director')
        ]
        
        for username, password, role, full_name in default_users:
            password_hash = self._hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, password_hash, role, full_name) VALUES (?, ?, ?, ?)",
                (username, password_hash, role, full_name)
            )
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self, username: str, password: str) -> bool:
        """Authenticate user"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        password_hash = self._hash_password(password)
        cursor.execute(
            "SELECT user_id, username, role, full_name FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash)
        )
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            self.current_user = {
                'user_id': user[0],
                'username': user[1],
                'role': user[2],
                'full_name': user[3]
            }
            print(f"✅ Welcome, {user[3]} ({user[2]})!")
            return True
        else:
            print("❌ Invalid username or password")
            return False
    
    def logout(self):
        """Logout current user"""
        if self.current_user:
            print(f"👋 Goodbye, {self.current_user['full_name']}!")
            self.current_user = None
        else:
            print("❌ No user is currently logged in")
    
    def get_current_user(self) -> Optional[Dict]:
        """Get current logged in user information"""
        return self.current_user
    
    def has_permission(self, required_role: str) -> bool:
        """Check if current user has required role permissions"""
        if not self.current_user:
            return False
        
        role_hierarchy = {'admin': 3, 'officer': 2, 'director': 1}
        current_role_level = role_hierarchy.get(self.current_user['role'], 0)
        required_role_level = role_hierarchy.get(required_role, 0)
        
        return current_role_level >= required_role_level
    
    def change_password(self, current_password: str, new_password: str) -> bool:
        """Change current user's password"""
        if not self.current_user:
            print("❌ No user is logged in")
            return False
        
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Verify current password
        current_hash = self._hash_password(current_password)
        cursor.execute(
            "SELECT user_id FROM users WHERE user_id = ? AND password_hash = ?",
            (self.current_user['user_id'], current_hash)
        )
        
        if not cursor.fetchone():
            print("❌ Current password is incorrect")
            conn.close()
            return False
        
        # Update to new password
        new_hash = self._hash_password(new_password)
        cursor.execute(
            "UPDATE users SET password_hash = ? WHERE user_id = ?",
            (new_hash, self.current_user['user_id'])
        )
        
        conn.commit()
        conn.close()
        print("✅ Password changed successfully!")
        return True
    