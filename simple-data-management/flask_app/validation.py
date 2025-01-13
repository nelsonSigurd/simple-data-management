from datetime import datetime

def validate_dateOfBirth(date_of_birth):
    try:
        parsed_date = datetime.strptime(date_of_birth, "%Y-%m-%d")
        if parsed_date > datetime.now():  # Date cannot be in the future
            return False, "Date of birth cannot be in the future."
        return True, None
    except ValueError:
        return False, "Invalid date format or incorrect date. Please use YYYY-MM-DD."

def validate_name(name: str) -> tuple[bool, str | None]:
    if not name.strip():
        return False, "Input cannot be empty. Please try again."
    if len(name) < 2 or len(name) > 50:
        return False, "Name must be between 2 and 50 characters long."
    if " " in name:
        return False, "Name must not contain spaces."
    if not name.isalpha():
        return False, "Name must contain only alphabetical characters."
    return True, None  # Valid name