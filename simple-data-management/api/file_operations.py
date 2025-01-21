import os
import csv

CSV_FILE = 'students.csv'

# Ensure the CSV file exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["First Name", "Last Name", "Date of Birth"])  # Add header

def read_records():
    records = []
    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header row

            for idx, row in enumerate(reader, start=1):
                if len(row) == 3:  # Fully valid row
                    records.append({"index": idx, "first_name": row[0], "last_name": row[1], "date_of_birth": row[2]})
            
            print("Records read from CSV:", records) 

        return records, None  # Return records and no error
    except FileNotFoundError:
        return [], f"The file '{CSV_FILE}' does not exist."
    except Exception as e:
        return [], f"An error occurred: {e}"

def write_records(records):
    try:
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["First Name", "Last Name", "Date of Birth"])  # Write header
            for record in records:
                writer.writerow([record["first_name"], record["last_name"], record["date_of_birth"]])
        return None
    except Exception as e:
        return f"An error occurred while writing to the file: {e}"