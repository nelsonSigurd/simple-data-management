from .file_operations import read_records, write_records

def delete_record(record_number):
    records, error = read_records()
    if error:
        return error
    if not records:
        return "No records to delete."

    if 1 <= record_number <= len(records):
        del records[record_number - 1]
        return write_records(records)
    else:
        return "Invalid record number. Please enter a valid number."
