from .file_operations import read_records

def get_all_records():
    records, error = read_records()
    if error:
        return None, error
    return records, None