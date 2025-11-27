import sqlite3
from typing import List, Dict, Tuple
import matplotlib.pyplot as plt
import pandas as pd

class AnalyticsService:
    def __init__(self, db_path: str = "student_wellbeing.db"):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
    
    def calculate_average_attendance(self, student_id: int) -> float:
        """Calculate average attendance percentage for a student"""
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT COUNT(*) as total, 
                   SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) as present
            FROM attendance 
            WHERE student_id = ?
        ''', (student_id,))
        
        result = cursor.fetchone()
        if result['total'] > 0:
            return (result['present'] / result['total']) * 100
        return 0.0
    
    def get_stress_trends(self, student_id: int) -> List[Dict]:
        """Get stress level trends over time for a student"""
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT week_number, stress_level, hours_slept
            FROM wellbeing_surveys 
            WHERE student_id = ?
            ORDER BY week_number
        ''', (student_id,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def identify_high_stress_weeks(self, student_id: int, threshold: int = 4) -> List[Dict]:
        """Identify weeks where stress level is above threshold"""
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT week_number, stress_level, hours_slept, additional_notes
            FROM wellbeing_surveys 
            WHERE student_id = ? AND stress_level >= ?
            ORDER BY week_number
        ''', (student_id, threshold))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_student_performance_summary(self, student_id: int) -> Dict:
        """Get comprehensive performance summary for a student"""
        cursor = self.connection.cursor()
        
        # Attendance summary
        cursor.execute('''
            SELECT COUNT(*) as total_classes,
                   SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) as attended
            FROM attendance WHERE student_id = ?
        ''', (student_id,))
        attendance = cursor.fetchone()
        
        # Wellbeing summary
        cursor.execute('''
            SELECT AVG(stress_level) as avg_stress,
                   AVG(hours_slept) as avg_sleep
            FROM wellbeing_surveys WHERE student_id = ?
        ''', (student_id,))
        wellbeing = cursor.fetchone()
        
        # Coursework summary
        cursor.execute('''
            SELECT COUNT(*) as total_assignments,
                   AVG(grade) as avg_grade
            FROM coursework 
            WHERE student_id = ? AND grade IS NOT NULL
        ''', (student_id,))
        coursework = cursor.fetchone()
        
        return {
            'attendance_rate': (attendance['attended'] / attendance['total_classes'] * 100) if attendance['total_classes'] > 0 else 0,
            'average_stress': wellbeing['avg_stress'] or 0,
            'average_sleep': wellbeing['avg_sleep'] or 0,
            'average_grade': coursework['avg_grade'] or 0,
            'assignments_completed': coursework['total_assignments'] or 0
        }
    
    def plot_stress_over_time(self, student_id: int):
        """Generate stress level visualization over time"""
        trends = self.get_stress_trends(student_id)
        if not trends:
            print("No survey data available for this student")
            return
        
        weeks = [item['week_number'] for item in trends]
        stress_levels = [item['stress_level'] for item in trends]
        sleep_hours = [item['hours_slept'] for item in trends]
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        # Stress levels plot
        ax1.plot(weeks, stress_levels, marker='o', color='red', linewidth=2)
        ax1.set_title(f'Stress Levels Over Time - Student {student_id}')
        ax1.set_xlabel('Week Number')
        ax1.set_ylabel('Stress Level (1-5)')
        ax1.grid(True)
        ax1.set_ylim(1, 5)
        
        # Sleep hours plot
        ax2.plot(weeks, sleep_hours, marker='s', color='blue', linewidth=2)
        ax2.set_title(f'Sleep Hours Over Time - Student {student_id}')
        ax2.set_xlabel('Week Number')
        ax2.set_ylabel('Hours Slept')
        ax2.grid(True)
        
        plt.tight_layout()
        plt.savefig(f'student_{student_id}_wellbeing.png')
        plt.show()
    
    def plot_attendance_trend(self, student_id: int):
        """Generate attendance trend visualization"""
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT week_number, 
                   SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) as present,
                   COUNT(*) as total
            FROM attendance 
            WHERE student_id = ?
            GROUP BY week_number
            ORDER BY week_number
        ''', (student_id,))
        
        data = cursor.fetchall()
        if not data:
            print("No attendance data available for this student")
            return
        
        weeks = [item['week_number'] for item in data]
        attendance_rates = [(item['present'] / item['total']) * 100 for item in data]
        
        plt.figure(figsize=(10, 6))
        plt.plot(weeks, attendance_rates, marker='o', color='green', linewidth=2)
        plt.title(f'Attendance Rate Over Time - Student {student_id}')
        plt.xlabel('Week Number')
        plt.ylabel('Attendance Rate (%)')
        plt.grid(True)
        plt.ylim(0, 100)
        
        plt.tight_layout()
        plt.savefig(f'student_{student_id}_attendance.png')
        plt.show()
    
    def generate_wellbeing_report(self, student_id: int):
        """Generate a comprehensive wellbeing report"""
        summary = self.get_student_performance_summary(student_id)
        high_stress_weeks = self.identify_high_stress_weeks(student_id)
        
        print(f"\n📊 Wellbeing Report - Student {student_id}")
        print("=" * 40)
        print(f"Attendance Rate: {summary['attendance_rate']:.1f}%")
        print(f"Average Stress Level: {summary['average_stress']:.1f}/5")
        print(f"Average Sleep: {summary['average_sleep']:.1f} hours")
        print(f"Average Grade: {summary['average_grade']:.1f}%")
        print(f"Assignments Completed: {summary['assignments_completed']}")
        
        if high_stress_weeks:
            print(f"\n⚠️  High Stress Weeks ({len(high_stress_weeks)}):")
            for week in high_stress_weeks:
                print(f"  Week {week['week_number']}: Stress {week['stress_level']}/5, Sleep {week['hours_slept']} hours")
        
        # Generate visualizations
        self.plot_stress_over_time(student_id)
        self.plot_attendance_trend(student_id)
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()