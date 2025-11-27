# Student Wellbeing System Requirements

## Core Functionality
- Student data management (CRUD operations)
- Attendance recording and tracking
- Wellbeing survey data collection
- Basic analytics and reporting
- Data visualization

## Data Collection
- Weekly attendance records
- Coursework submission status
- Wellbeing survey responses
- Student information

## Database Schema Design

### Tables:

**students**
- student_id (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- name (TEXT, NOT NULL)
- email (TEXT, UNIQUE, NOT NULL)
- created_date (DATE, DEFAULT CURRENT_DATE)

**attendance**
- attendance_id (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- student_id (INTEGER, FOREIGN KEY)
- week_number (INTEGER)
- module_code (TEXT)
- status (TEXT) - 'Present' or 'Absent'
- date_recorded (DATE, DEFAULT CURRENT_DATE)

**wellbeing_surveys**
- survey_id (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- student_id (INTEGER, FOREIGN KEY)
- week_number (INTEGER)
- stress_level (INTEGER) - 1 to 5
- hours_slept (REAL)
- additional_notes (TEXT)
- survey_date (DATE, DEFAULT CURRENT_DATE)

**coursework**
- coursework_id (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- student_id (INTEGER, FOREIGN KEY)
- module_code (TEXT)
- assignment_name (TEXT)
- submission_date (DATE)
- status (TEXT) - 'Submitted', 'Late', 'Missing'
- grade (REAL) - Optional