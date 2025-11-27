class Student:
    def __init__(self, student_id, name, email):
        self.student_id = student_id
        self.name = name
        self.email = email
    
    def to_dict(self):
        return {
            'student_id': self.student_id,
            'name': self.name,
            'email': self.email
        }
    