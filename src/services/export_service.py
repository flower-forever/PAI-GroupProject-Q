import csv
import json
import pandas as pd
from datetime import datetime
from typing import List, Dict
import sqlite3

class ExportService:
    def __init__(self, db_path: str = "student_wellbeing.db"):
        self.db_path = db_path
    
    def export_students_to_csv(self, filename: str = None) -> str:
        """Export all students to CSV"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"students_export_{timestamp}.csv"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(column_names)
            writer.writerows(students)
        
        conn.close()
        print(f"✅ Students exported to {filename}")
        return filename
    
    def export_attendance_report(self, filename: str = None) -> str:
        """Export attendance summary report to CSV"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"attendance_report_{timestamp}.csv"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = """
            SELECT 
                s.student_id,
                s.name as student_name,
                s.email,
                COUNT(a.attendance_id) as total_classes,
                SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) as classes_attended,
                ROUND((SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) * 100.0 / COUNT(a.attendance_id)), 2) as attendance_rate
            FROM students s
            LEFT JOIN attendance a ON s.student_id = a.student_id
            GROUP BY s.student_id, s.name, s.email
            ORDER BY attendance_rate DESC
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(column_names)
            writer.writerows(results)
        
        conn.close()
        print(f"✅ Attendance report exported to {filename}")
        return filename
    
    def export_wellbeing_data(self, filename: str = None) -> str:
        """Export wellbeing survey data to CSV"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"wellbeing_data_{timestamp}.csv"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = """
            SELECT 
                s.student_id,
                s.name as student_name,
                w.week_number,
                w.stress_level,
                w.hours_slept,
                w.additional_notes,
                w.survey_date
            FROM wellbeing_surveys w
            JOIN students s ON w.student_id = s.student_id
            ORDER BY s.name, w.week_number
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(column_names)
            writer.writerows(results)
        
        conn.close()
        print(f"✅ Wellbeing data exported to {filename}")
        return filename
    
    def export_high_stress_report(self, stress_threshold: int = 4, filename: str = None) -> str:
        """Export report of students with high stress levels"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"high_stress_report_{timestamp}.csv"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = """
            SELECT 
                s.student_id,
                s.name as student_name,
                s.email,
                w.week_number,
                w.stress_level,
                w.hours_slept,
                w.additional_notes,
                w.survey_date
            FROM wellbeing_surveys w
            JOIN students s ON w.student_id = s.student_id
            WHERE w.stress_level >= ?
            ORDER BY w.stress_level DESC, s.name
        """
        
        cursor.execute(query, (stress_threshold,))
        results = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(column_names)
            writer.writerows(results)
        
        conn.close()
        print(f"✅ High stress report exported to {filename}")
        return filename
    
    def generate_comprehensive_report(self) -> Dict:
        """Generate a comprehensive system report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get basic statistics
        cursor.execute("SELECT COUNT(*) FROM students")
        total_students = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM attendance")
        total_attendance_records = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM wellbeing_surveys")
        total_surveys = cursor.fetchone()[0]
        
        cursor.execute("SELECT AVG(stress_level) FROM wellbeing_surveys")
        avg_stress = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT AVG(hours_slept) FROM wellbeing_surveys")
        avg_sleep = cursor.fetchone()[0] or 0
        
        cursor.execute('''
            SELECT COUNT(*) FROM wellbeing_surveys WHERE stress_level >= 4
        ''')
        high_stress_count = cursor.fetchone()[0]
        
        conn.close()
        
        report = {
            'total_students': total_students,
            'total_attendance_records': total_attendance_records,
            'total_wellbeing_surveys': total_surveys,
            'average_stress_level': round(avg_stress, 2),
            'average_sleep_hours': round(avg_sleep, 2),
            'high_stress_cases': high_stress_count,
            'report_generated': datetime.now().isoformat()
        }
        
        # Save report as JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_filename = f"comprehensive_report_{timestamp}.json"
        
        with open(json_filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(report, jsonfile, indent=2)
        
        print(f"✅ Comprehensive report generated: {json_filename}")
        return report