import sqlite3
import os
from typing import List, Dict, Optional

class DatabaseHandler:
    def __init__(self, db_path: str = "student_wellbeing.db"):
        self.db_path = db_path
        self.connection = None
        self.connect()
        self.create_tables()
    
    def connect(self) -> bool:
        """Establish database connection"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # This enables column access by name
            print(f"✅ Connected to database: {self.db_path}")
            return True
        except sqlite3.Error as e:
            print(f"❌ Database connection error: {e}")
            return False
    
    def create_tables(self) -> bool:
        """Create all necessary tables"""
        try:
            cursor = self.connection.cursor()
            
            # Students table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    created_date DATE DEFAULT CURRENT_DATE
                )
            ''')
            
            # Attendance table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS attendance (
                    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER,
                    week_number INTEGER,
                    module_code TEXT,
                    status TEXT CHECK(status IN ('Present', 'Absent')),
                    date_recorded DATE DEFAULT CURRENT_DATE,
                    FOREIGN KEY (student_id) REFERENCES students(student_id)
                )
            ''')
            
            # Wellbeing surveys table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS wellbeing_surveys (
                    survey_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER,
                    week_number INTEGER,
                    stress_level INTEGER CHECK(stress_level >= 1 AND stress_level <= 5),
                    hours_slept REAL,
                    additional_notes TEXT,
                    survey_date DATE DEFAULT CURRENT_DATE,
                    FOREIGN KEY (student_id) REFERENCES students(student_id)
                )
            ''')
            
            # Coursework table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS coursework (
                    coursework_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER,
                    module_code TEXT,
                    assignment_name TEXT,
                    submission_date DATE,
                    status TEXT CHECK(status IN ('Submitted', 'Late', 'Missing')),
                    grade REAL,
                    FOREIGN KEY (student_id) REFERENCES students(student_id)
                )
            ''')
            
            self.connection.commit()
            print("✅ Database tables created successfully")
            return True
            
        except sqlite3.Error as e:
            print(f"❌ Error creating tables: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("✅ Database connection closed")
    
    # Student CRUD operations
    def add_student(self, name: str, email: str) -> int:
        """Add a new student and return their ID"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO students (name, email) VALUES (?, ?)",
                (name, email)
            )
            self.connection.commit()
            student_id = cursor.lastrowid
            print(f"✅ Student added with ID: {student_id}")
            return student_id
        except sqlite3.Error as e:
            print(f"❌ Error adding student: {e}")
            return -1
    
    def get_all_students(self) -> List[Dict]:
        """Get all students"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM students")
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"❌ Error fetching students: {e}")
            return []
    
    def get_student_by_id(self, student_id: int) -> Optional[Dict]:
        """Get a specific student by ID"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"❌ Error fetching student: {e}")
            return None

    # Attendance CRUD operations
    def record_attendance(self, student_id: int, week_number: int, module_code: str, status: str) -> int:
        """Record attendance for a student"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """INSERT INTO attendance (student_id, week_number, module_code, status) 
                   VALUES (?, ?, ?, ?)""",
                (student_id, week_number, module_code, status)
            )
            self.connection.commit()
            attendance_id = cursor.lastrowid
            print(f"✅ Attendance recorded with ID: {attendance_id}")
            return attendance_id
        except sqlite3.Error as e:
            print(f"❌ Error recording attendance: {e}")
            return -1

    def get_attendance_by_student(self, student_id: int) -> List[Dict]:
        """Get all attendance records for a specific student"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT * FROM attendance WHERE student_id = ? ORDER BY week_number",
                (student_id,)
            )
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"❌ Error fetching attendance: {e}")
            return []

    # Wellbeing survey CRUD operations
    def add_wellbeing_survey(self, student_id: int, week_number: int, stress_level: int, 
                           hours_slept: float, additional_notes: str = "") -> int:
        """Add a wellbeing survey response"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """INSERT INTO wellbeing_surveys (student_id, week_number, stress_level, hours_slept, additional_notes) 
                   VALUES (?, ?, ?, ?, ?)""",
                (student_id, week_number, stress_level, hours_slept, additional_notes)
            )
            self.connection.commit()
            survey_id = cursor.lastrowid
            print(f"✅ Wellbeing survey added with ID: {survey_id}")
            return survey_id
        except sqlite3.Error as e:
            print(f"❌ Error adding wellbeing survey: {e}")
            return -1

    def get_surveys_by_student(self, student_id: int) -> List[Dict]:
        """Get all wellbeing surveys for a specific student"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT * FROM wellbeing_surveys WHERE student_id = ? ORDER BY week_number",
                (student_id,)
            )
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"❌ Error fetching wellbeing surveys: {e}")
            return []

    # Coursework CRUD operations
    def add_coursework(self, student_id: int, module_code: str, assignment_name: str, 
                      submission_date: str, status: str, grade: float = None) -> int:
        """Add coursework information"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """INSERT INTO coursework (student_id, module_code, assignment_name, submission_date, status, grade) 
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (student_id, module_code, assignment_name, submission_date, status, grade)
            )
            self.connection.commit()
            coursework_id = cursor.lastrowid
            print(f"✅ Coursework added with ID: {coursework_id}")
            return coursework_id
        except sqlite3.Error as e:
            print(f"❌ Error adding coursework: {e}")
            return -1

    def get_coursework_by_student(self, student_id: int) -> List[Dict]:
        """Get all coursework for a specific student"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT * FROM coursework WHERE student_id = ? ORDER BY submission_date",
                (student_id,)
            )
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"❌ Error fetching coursework: {e}")
            return []
            # Update operations
    def update_student(self, student_id: int, name: str = None, email: str = None) -> bool:
        """Update student information"""
        try:
            cursor = self.connection.cursor()
            updates = []
            params = []
            
            if name:
                updates.append("name = ?")
                params.append(name)
            if email:
                updates.append("email = ?")
                params.append(email)
            
            if not updates:
                return False
                
            params.append(student_id)
            query = f"UPDATE students SET {', '.join(updates)} WHERE student_id = ?"
            cursor.execute(query, params)
            self.connection.commit()
            
            if cursor.rowcount > 0:
                print(f"✅ Student {student_id} updated successfully")
                return True
            return False
            
        except sqlite3.Error as e:
            print(f"❌ Error updating student: {e}")
            return False

    def update_attendance(self, attendance_id: int, status: str = None) -> bool:
        """Update attendance record"""
        try:
            cursor = self.connection.cursor()
            query = "UPDATE attendance SET status = ? WHERE attendance_id = ?"
            cursor.execute(query, (status, attendance_id))
            self.connection.commit()
            
            if cursor.rowcount > 0:
                print(f"✅ Attendance record {attendance_id} updated")
                return True
            return False
            
        except sqlite3.Error as e:
            print(f"❌ Error updating attendance: {e}")
            return False

    # Delete operations
    def delete_student(self, student_id: int) -> bool:
        """Delete a student and all their related records"""
        try:
            cursor = self.connection.cursor()
            
            # Delete related records first (due to foreign key constraints)
            cursor.execute("DELETE FROM attendance WHERE student_id = ?", (student_id,))
            cursor.execute("DELETE FROM wellbeing_surveys WHERE student_id = ?", (student_id,))
            cursor.execute("DELETE FROM coursework WHERE student_id = ?", (student_id,))
            
            # Delete student
            cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
            self.connection.commit()
            
            if cursor.rowcount > 0:
                print(f"✅ Student {student_id} and all related records deleted")
                return True
            return False
            
        except sqlite3.Error as e:
            print(f"❌ Error deleting student: {e}")
            return False

    def delete_attendance(self, attendance_id: int) -> bool:
        """Delete a specific attendance record"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM attendance WHERE attendance_id = ?", (attendance_id,))
            self.connection.commit()
            
            if cursor.rowcount > 0:
                print(f"✅ Attendance record {attendance_id} deleted")
                return True
            return False
            
        except sqlite3.Error as e:
            print(f"❌ Error deleting attendance: {e}")
            return False

    def delete_wellbeing_survey(self, survey_id: int) -> bool:
        """Delete a wellbeing survey record"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM wellbeing_surveys WHERE survey_id = ?", (survey_id,))
            self.connection.commit()
            
            if cursor.rowcount > 0:
                print(f"✅ Wellbeing survey {survey_id} deleted")
                return True
            return False
            
        except sqlite3.Error as e:
            print(f"❌ Error deleting wellbeing survey: {e}")
            return False

    # Enhanced read operations
    def search_students(self, search_term: str) -> List[Dict]:
        """Search students by name or email"""
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT * FROM students 
                WHERE name LIKE ? OR email LIKE ?
                ORDER BY name
            """
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern))
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"❌ Error searching students: {e}")
            return []

    def get_all_attendance(self) -> List[Dict]:
        """Get all attendance records with student names"""
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT a.*, s.name as student_name
                FROM attendance a
                JOIN students s ON a.student_id = s.student_id
                ORDER BY a.week_number, s.name
            """
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"❌ Error fetching all attendance: {e}")
            return []