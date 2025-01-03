import os
import csv
from datetime import datetime

# Referencing the file
csv_file = 'people.csv'

# Ensure the CSV file exists
if not os.path.exists(csv_file):
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["First Name", "Last Name", "Date of Birth"])  # Add header


def read_records(file_name):
    records = []
    try:
        with open(file_name, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header row

            for idx, row in enumerate(reader, start=1):
                if len(row) == 3:  # Fully valid row
                    records.append({"index": idx, "first_name": row[0], "last_name": row[1], "date_of_birth": row[2]})
                else:
                    pass  # Skip malformed rows
        return records, None  # Return records and no error
    except FileNotFoundError:
        return [], f"The file '{file_name}' does not exist."
    except Exception as e:
        return [], f"An error occurred: {e}"


def create_record(file_name, first_name, last_name, date_of_birth):
    try:
        with open(file_name, mode='a+', newline='', encoding='utf-8') as file:
            file.seek(0)  # Move to the start of the file
            rows = list(csv.reader(file))

            # If the file is empty, write the header row
            if not rows:
                writer = csv.writer(file)
                writer.writerow(["First Name", "Last Name", "Date of Birth"])

            # Append the new record
            writer = csv.writer(file)
            writer.writerow([first_name, last_name, date_of_birth])
            return None  # No error
    except Exception as e:
        return f"An error occurred while adding the record: {e}"


def delete_record(file_name, record_number):
    try:
        records, error = read_records(file_name)
        if error:
            return error
        if not records:
            return "No records to delete."

        if 1 <= record_number <= len(records):
            # Remove the specified record
            del records[record_number - 1]
            # Write updated records back to the file
            with open(file_name, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["First Name", "Last Name", "Date of Birth"])  # Write header
                for record in records:
                    writer.writerow([record["first_name"], record["last_name"], record["date_of_birth"]])
            return None
        else:
            return "Invalid record number. Please enter a valid number."
    except Exception as e:
        return f"An error occurred while deleting the record: {e}"


def update_record(file_name, record_number, first_name, last_name, date_of_birth):
    try:
        records, error = read_records(file_name)
        if error:
            return error
        if not records:
            return "No records to update."

        if 1 <= record_number <= len(records):
            # Update the specific record
            records[record_number - 1]["first_name"] = first_name
            records[record_number - 1]["last_name"] = last_name
            records[record_number - 1]["date_of_birth"] = date_of_birth

            # Write the updated records back to the file
            with open(file_name, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["First Name", "Last Name", "Date of Birth"])  # Write header
                for record in records:
                    writer.writerow([record["first_name"], record["last_name"], record["date_of_birth"]])
            return None
        else:
            return "Invalid record number. Please enter a valid number."
    except Exception as e:
        return f"An error occurred while updating the record: {e}"


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


def get_record_length(file_name):
    try:
        with open(file_name, mode='r') as file:
            reader = csv.reader(file)
            return sum(1 for row in reader) - 1  # Subtract 1 for the header row
    except FileNotFoundError:
        return 0