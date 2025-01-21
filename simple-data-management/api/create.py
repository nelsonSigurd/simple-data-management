from .file_operations import read_records, write_records

def create_record(first_name, last_name, date_of_birth):
    records, error = read_records()
    if error:
        return error

    records.append({"first_name": first_name, "last_name": last_name, "date_of_birth": date_of_birth})
    return write_records(records)
