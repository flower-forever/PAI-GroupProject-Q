def format_percentage(value):
    return f"{value:.2f}%"

def validate_email(email):
    # Simple email validation
    return "@" in email and "." in email
