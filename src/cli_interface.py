from database.db_handler import DatabaseHandler
from services.analytics_service import AnalyticsService

class CLIInterface:
    def __init__(self):
        self.db = DatabaseHandler()
        self.analytics = AnalyticsService()
    
    def display_main_menu(self):
        """Display the main menu"""
        print("\n" + "="*50)
        print("    STUDENT WELLBEING SYSTEM")
        print("="*50)
        print("1. Student Management")
        print("2. Attendance Records") 
        print("3. Analytics & Reports")
        print("4. Search Data")
        print("5. Data Export")
        print("6. Authentication")
        print("0. Exit")
        print("="*50)
    
    def student_management_menu(self):
        """Simple student management"""
        print("\n--- Student Management ---")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Back")
        
        choice = input("\nEnter your choice: ").strip()
        if choice == "1":
            name = input("Enter student name: ")
            email = input("Enter student email: ")
            student_id = self.db.add_student(name, email)
            print(f"✅ Student added with ID: {student_id}")
        elif choice == "2":
            students = self.db.get_all_students()
            for student in students:
                print(f"ID: {student['student_id']}, Name: {student['name']}")
    
    def analytics_menu(self):
        """Simple analytics menu"""
        student_id = int(input("Enter student ID for analytics: "))
        self.analytics.generate_wellbeing_report(student_id)
    
    def search_menu(self):
        """Simple search"""
        search_term = input("Enter search term: ")
        results = self.db.search_students(search_term)
        for student in results:
            print(f"ID: {student['student_id']}, Name: {student['name']}")
    
    def export_menu(self):
        """Simple export menu"""
        from services.export_service import ExportService
        export = ExportService()
        export.export_students_to_csv()
        print("✅ Students exported to CSV")
    
    def authentication_menu(self):
        """Simple authentication"""
        from services.auth_service import AuthService
        auth = AuthService()
        username = input("Username: ")
        password = input("Password: ")
        if auth.login(username, password):
            print(f"✅ Welcome {auth.current_user['full_name']}!")
        else:
            print("❌ Login failed")
    
    def run(self):
        """Main application loop"""
        print("🚀 Student Wellbeing System - Command Line Interface")
        
        while True:
            self.display_main_menu()
            choice = input("\nEnter your choice (0-6): ").strip()
            
            if choice == "1":
                self.student_management_menu()
            elif choice == "2":
                print("Attendance menu - to be implemented")
            elif choice == "3":
                self.analytics_menu()
            elif choice == "4":
                self.search_menu()
            elif choice == "5":
                self.export_menu()
            elif choice == "6":
                self.authentication_menu()
            elif choice == "0":
                print("👋 Thank you for using Student Wellbeing System!")
                break
            else:
                print("❌ Invalid choice. Please try again.")
        
        self.db.close()
        self.analytics.close()