from .file_operations import read_records, write_records

def update_record(record_number, first_name, last_name, date_of_birth):
    records, error = read_records()
    if error:
        return error
    if not records:
        return "No records to update."

    if 1 <= record_number <= len(records):
        records[record_number - 1]["first_name"] = first_name
        records[record_number - 1]["last_name"] = last_name
        records[record_number - 1]["date_of_birth"] = date_of_birth
        return write_records(records)
    else:
        return "Invalid record number. Please enter a valid number."
