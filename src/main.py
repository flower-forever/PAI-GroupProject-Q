from database.db_handler import DatabaseHandler
from services.analytics_service import AnalyticsService

def setup_sample_data():
    """Create sample data for demonstration"""
    db = DatabaseHandler()
    
    # Add sample student
    student_id = db.add_student("Alex Johnson", "alex.johnson@university.com")
    
    # Add attendance records
    for week in range(1, 9):
        status = "Present" if week != 3 and week != 6 else "Absent"
        db.record_attendance(student_id, week, "CS101", status)
    
    # Add wellbeing surveys
    wellbeing_data = [
        (1, 2, 7.5, "Feeling good"),
        (2, 3, 6.5, "Moderate stress"),
        (3, 4, 5.0, "Exams coming up"),
        (4, 2, 8.0, "Well rested"),
        (5, 5, 4.5, "Very stressed"),
        (6, 3, 7.0, "Recovering"),
        (7, 2, 7.5, "Good balance"),
        (8, 4, 6.0, "Project deadline")
    ]
    
    for week, stress, sleep, notes in wellbeing_data:
        db.add_wellbeing_survey(student_id, week, stress, sleep, notes)
    
    # Add coursework
    db.add_coursework(student_id, "CS101", "Python Basics", "2024-01-20", "Submitted", 88.0)
    db.add_coursework(student_id, "CS101", "Data Structures", "2024-02-10", "Submitted", 92.0)
    db.add_coursework(student_id, "CS101", "Final Project", "2024-03-01", "Submitted", 85.0)
    
    db.close()
    return student_id

def main():
    print("Student Wellbeing Analytics System")
    print("==================================")
    
    # Setup sample data
    print("\nSetting up sample data...")
    student_id = setup_sample_data()
    print(f"Sample student created with ID: {student_id}")
    
    # Initialize analytics service
    analytics = AnalyticsService()
    
    # Demo analytics features
    print(f"\nAnalytics for Student {student_id}:")
    print("-" * 30)
    
    # Basic calculations
    attendance_rate = analytics.calculate_average_attendance(student_id)
    print(f"Average Attendance: {attendance_rate:.1f}%")
    
    # Performance summary
    summary = analytics.get_student_performance_summary(student_id)
    print(f"Average Stress Level: {summary['average_stress']:.1f}/5")
    print(f"Average Sleep: {summary['average_sleep']:.1f} hours")
    print(f"Average Grade: {summary['average_grade']:.1f}%")
    
    # High stress analysis
    high_stress_weeks = analytics.identify_high_stress_weeks(student_id)
    print(f"High stress weeks identified: {len(high_stress_weeks)}")
    
    # Generate comprehensive report
    print(f"\nGenerating comprehensive report...")
    analytics.generate_wellbeing_report(student_id)
    
    analytics.close()
    print("\nAnalytics demonstration completed!")

if __name__ == "__main__":
    main()