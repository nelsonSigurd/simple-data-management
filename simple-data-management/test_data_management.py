import unittest
from unittest.mock import patch
import csv
import os
from tempfile import NamedTemporaryFile
from data_management import read_records, create_record, delete_record,  update_record, validate_dateOfBirth, get_valid_dateOfBirth, validate_name, get_valid_name, get_valid_record_number, get_record_length
from datetime import datetime, timedelta

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        # Create temp file for testing
        self.temp_file = NamedTemporaryFile(mode='w+', delete=False, newline='', encoding='utf-8')
        self.file_name = self.temp_file.name

    def tearDown(self):
        # Close the file if it is still open
        try:
            self.temp_file.close()
        except Exception:
            pass  # Ignore errors if the file is already closed

        # Delete the file if it exists
        if os.path.exists(self.file_name):
            os.unlink(self.file_name)

    def add_single_record (self):
        writer = csv.writer(self.temp_file)
        writer.writerow(["First Name", "Last Name", "Date of Birth"])
        writer.writerow(["John", "Doe", "1990-01-01"])
        self.temp_file.seek(0)

class TestReadRecords(BaseTestCase):

    def test_empty_file(self):
        # Write only the header to simulate an empty file
        writer = csv.writer(self.temp_file)
        writer.writerow(["First Name", "Last Name", "Date of Birth"])
        self.temp_file.seek(0)

        # Capture logging output
        with self.assertLogs(level='INFO') as log:
            read_records(self.file_name)
        self.assertIn("Current Records in File:", log.output[0])

    
    def test_single_record(self):
        # Write one record
        self.add_single_record()

        # Capture logging output
        with self.assertLogs(level='INFO') as log:
            read_records(self.file_name)
        # Check the specific log entry
        self.assertIn("INFO:root:1. John Doe, Date of Birth: 1990-01-01", log.output)



    def test_multiple_records(self):
        # Write multiple records
        writer = csv.writer(self.temp_file)
        writer.writerow(["First Name", "Last Name", "Date of Birth"])
        writer.writerow(["John", "Doe", "1990-01-01"])
        writer.writerow(["Jane", "Smith", "1985-05-15"])
        self.temp_file.seek(0)

        # Capture printed output
        with self.assertLogs(level='INFO') as log:
            read_records(self.file_name)

        # Check for each record's log message
        self.assertIn("INFO:root:1. John Doe, Date of Birth: 1990-01-01", log.output)
        self.assertIn("INFO:root:2. Jane Smith, Date of Birth: 1985-05-15", log.output)

        
    def test_missing_file(self):
        # Close the temporary file to release the handle
        self.temp_file.close()

        # Delete the temporary file to simulate a missing file
        os.unlink(self.file_name)

        # Capture logging output
        with self.assertLogs(level='ERROR') as log:
            read_records(self.file_name)

        # Check that the expected message is in the captured logs
        self.assertIn(f"ERROR:root:The file '{self.file_name}' does not exist.", log.output)

    def test_corrupted_data(self):
        # Creating incorrect formatted records
        writer = csv.writer(self.temp_file)
        writer.writerow(["First Name", "Last Name", "Date of Birth"])  # Header row
        writer.writerow(["John", "Doe"])  # Missing date of birth
        writer.writerow(["Jane", "Smith", "1985-05-15"])  # Valid row
        writer.writerow(["OnlyOneColumn"])  # Corrupted row
        self.temp_file.seek(0)

        # Capture logging output
        with self.assertLogs(level='INFO') as log:
            read_records(self.file_name)

        # Check that valid and partial rows are logged
        self.assertIn("INFO:root:1. John Doe, Date of Birth: Unknown", log.output)  # Partial row
        self.assertIn("INFO:root:2. Jane Smith, Date of Birth: 1985-05-15", log.output)

        # Check that corrupted rows are logged as errors
        self.assertIn("ERROR:root:Malformed row skipped: ['OnlyOneColumn']", log.output)


class TestCreateRecord(BaseTestCase):

    def test_single_valid_record(self):
        # Add a single valid record
        create_record(self.file_name, "John", "Doe", "1990-01-01")

        # Verify the record is added correctly
        with open(self.file_name, mode='r') as file:
            rows = list(csv.reader(file))
        self.assertEqual(len(rows), 2)  # Header + 1 record
        self.assertEqual(rows[1], ["John", "Doe", "1990-01-01"])

    def test_multiple_records(self):
        # Add multiple records
        create_record(self.file_name, "John", "Doe", "1990-01-01")
        create_record(self.file_name, "Jane", "Smith", "1985-05-15")

        with open(self.file_name, mode='r') as file:
            rows = list(csv.reader(file))
        self.assertEqual(len(rows), 3)  # Header + 2 records
        self.assertEqual(rows[1], ["John", "Doe", "1990-01-01"])
        self.assertEqual(rows[2], ["Jane", "Smith", "1985-05-15"])

class TestDeleteRecord(BaseTestCase):  

    def test_delete_single_record(self):

        self.add_single_record()

        # Delete the record
        delete_record(self.file_name, 1)

        # Verify the file is now empty (except for the header)
        with open(self.file_name, mode='r') as file:
            rows = list(csv.reader(file))
            self.assertEqual(len(rows), 1)  # Only the header remains

    def test_delete_one_of_multiple(self):
        # Add multiple records
        writer = csv.writer(self.temp_file)
        writer.writerow(["First Name", "Last Name", "Date of Birth"])
        writer.writerow(["John", "Doe", "1990-01-01"])
        writer.writerow(["Jane", "Smith", "1985-05-15"])
        writer.writerow(["Emily", "Brown", "2000-07-20"])
        self.temp_file.seek(0)

        # Delete the second record
        delete_record(self.file_name, 2)

        # Verify the remaining records
        with open(self.file_name, mode='r') as file:
            rows = list(csv.reader(file))
        self.assertEqual(len(rows), 3)  # Header + 2 records
        self.assertEqual(rows[1], ["John", "Doe", "1990-01-01"])
        self.assertEqual(rows[2], ["Emily", "Brown", "2000-07-20"])

    def test_no_records_to_delete(self):
        # Create an empty file with only the header
        writer = csv.writer(self.temp_file)
        writer.writerow(["First Name", "Last Name", "Date of Birth"])
        self.temp_file.seek(0)

        # Attempt to delete a record
        with self.assertLogs(level='INFO') as log:
            delete_record(self.file_name, 1)

        # Verify the file remains unchanged
        with open(self.file_name, mode='r') as file:
            rows = list(csv.reader(file))
        self.assertEqual(len(rows), 1)  # Only the header remains
        self.assertIn("ERROR:root:No records to delete.", log.output)


    def delete_first_record(self):
        # Add multiple records
        writer = csv.writer(self.temp_file)
        writer.writerow(["First Name", "Last Name", "Date of Birth"])
        writer.writerow(["John", "Doe", "1990-01-01"])
        writer.writerow(["Jane", "Smith", "1985-05-15"])
        self.temp_file.seek(0)

        # Delete the first record
        delete_record(self.file_name, 1)

        with open(self.file_name, mode='r') as file:
            rows = list(csv.reader(file))    
        self.assertEqual(len(rows), 2)  # Header + 1 record 
        self.assertEqual(rows[1], ["Jane", "Smith", "1985-05-15"])

    def test_delete_last_record(self):
        # Add multiple records
        writer = csv.writer(self.temp_file)
        writer.writerow(["First Name", "Last Name", "Date of Birth"])
        writer.writerow(["John", "Doe", "1990-01-01"])
        writer.writerow(["Jane", "Smith", "1985-05-15"])
        self.temp_file.seek(0)

        # Delete the last record
        delete_record(self.file_name, 2)

        with open(self.file_name, mode='r') as file:
            rows = list(csv.reader(file))
        self.assertEqual(len(rows), 2)  # Header + 1 record
        self.assertEqual(rows[1], ["John", "Doe", "1990-01-01"])


class TestUpdateRecord(BaseTestCase):

    def test_update_record(self):

        self.add_single_record()

        # Update the record
        update_record(self.file_name, 1, "Jane", "Smith", "1985-05-15")

        with open(self.file_name, mode='r') as file:
            rows = list(csv.reader(file))
        self.assertEqual(len(rows), 2)  # Header + 1 record
        self.assertEqual(rows[1], ["Jane", "Smith", "1985-05-15"])

    def test_update_nonexistent_record(self):

        self.add_single_record()

        # Update a non-existent record
        with self.assertLogs(level='INFO') as log:
            update_record(self.file_name, 2, "Jane", "Smith", "1985-05-15")

        # Verify the record is not updated
        with open(self.file_name, mode='r') as file:
            rows = list(csv.reader(file))
        self.assertEqual(len(rows), 2)  # Header + 1 record
        self.assertEqual(rows[1], ["John", "Doe", "1990-01-01"])
        self.assertIn("ERROR:root:Invalid record number: 2. Please enter a valid number.", log.output)

    def test_no_records_to_update(self):
        # Create an empty file with only the header
        writer = csv.writer(self.temp_file)
        writer.writerow(["First Name", "Last Name", "Date of Birth"])
        self.temp_file.seek(0)

        # Attempt to update a record
        with self.assertLogs(level='INFO') as log:
            update_record(self.file_name, 1, "Jane", "Smith", "1985-05-15")

        
        with open(self.file_name, mode='r') as file:
            rows = list(csv.reader(file))
        self.assertEqual(len(rows), 1)  # Only the header remains
        self.assertIn("ERROR:root:No records to update.", log.output)

    
class TestValidateDateOfBirth(BaseTestCase):
    def test_valid_date(self):
        result, error = validate_dateOfBirth("1985-05-15")
        self.assertTrue(result)
        self.assertIsNone(error)

    def test_invalid_format(self):
        result, error = validate_dateOfBirth("20-05-1985")
        self.assertFalse(result)
        self.assertEqual(error, "Invalid date format or incorrect date. Please use YYYY-MM-DD.")

    def test_future_date(self):
        future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        result, error = validate_dateOfBirth(future_date)
        self.assertFalse(result)
        self.assertEqual(error, "Date of birth cannot be in the future.")

class TestGetValidDateOfBirth(BaseTestCase):

    def test_get_valid_dateOfBirth_invalid_then_valid(self):
        with patch("builtins.input", side_effect=["invalid-date","15-05-1985", "1985-05-15"]):  # Invalid inputs first, then valid input
            result = get_valid_dateOfBirth("Enter date:")
            self.assertEqual(result, "1985-05-15")

    def test_get_valid_dateOfBirth_with_spaces(self):
        with patch("builtins.input", return_value=" 1985-05-15 "):
            result = get_valid_dateOfBirth("Enter date:")
            self.assertEqual(result, "1985-05-15")

    def test_get_valid_dateOfBirth_empty_input(self):
        with patch("builtins.input", side_effect=["", "", "1985-05-15"]):  # Empty inputs first, then valid
            result = get_valid_dateOfBirth("Enter date:")
            self.assertEqual(result, "1985-05-15")


class TestValidateName(BaseTestCase):

    def test_valid_first_name(self):
        result, error = validate_name("John")
        self.assertTrue(result)
        self.assertIsNone(error)

    def test_name_with_spaces(self):
        result, error = validate_name(" John Doe ")  # Name spaces
        self.assertFalse(result)
        self.assertEqual(error, "Name must not contain spaces.")

    def test_name_with_special_characters(self):
        result, error = validate_name("John@Doe")  # Name with special characters
        self.assertFalse(result)
        self.assertEqual(error, "Name must contain only alphabetical characters.")

    def test_min_name_length(self):
        result, error = validate_name("J")  # Name too short
        self.assertFalse(result)
        self.assertEqual(error, "Name must be between 2 and 50 characters long.")

    def test_max_name_length(self):
        result, error = validate_name("John" * 51)  # Name too long
        self.assertFalse(result)
        self.assertEqual(error, "Name must be between 2 and 50 characters long.")

class TestGetValidName(BaseTestCase):
    def test_valid_name(self):
        with patch("builtins.input", return_value="Joey"):
            result = get_valid_name("Enter name:")
            self.assertEqual(result, "Joey")

    def test_cancel_keyword(self):
        with patch("builtins.input", return_value="cancel"):
            with self.assertLogs(level="INFO") as log:
                result = get_valid_name("Enter name:")
                self.assertIsNone(result) # function returns None
                self.assertIn("INFO:root:Operation canceled. Returning to menu", log.output)

    def test_cancel_keyword_with_spaces(self):
        with patch("builtins.input", return_value="  cancel  "):
            with self.assertLogs(level="INFO") as log:
                result = get_valid_name("Enter name:")
                self.assertIsNone(result) # function returns None
                self.assertIn("INFO:root:Operation canceled. Returning to menu", log.output)

    def test_valid_name_with_spaces(self):
        with patch("builtins.input", return_value="  Joey  "):
            result = get_valid_name("Enter name:")
            self.assertEqual(result, "Joey")

    def test_input_with_non_alpha(self):
        with patch("builtins.input", side_effect=["John123", "Alice"]):  # Invalid input first, then valid
            with self.assertLogs(level="ERROR") as log:  # Capture error logs
                result = get_valid_name("Enter name:")
                self.assertEqual(result, "Alice")  # Ensure valid input is eventually returned
                self.assertIn("ERROR:root:Name must contain only alphabetical characters.", log.output)

class TestGetValidRecordNumber(BaseTestCase):

    def test_valid_record_number(self):

        writer = csv.writer(self.temp_file)
        writer.writerow(["First Name", "Last Name", "Date of Birth"]) 
        writer.writerow(["John", "Doe", "1990-01-01"])
        writer.writerow(["Jane", "Smith", "1985-05-15"])
        writer.writerow(["Emily", "Davis", "2000-03-22"])
        self.temp_file.seek(0)

        # Test for a valid record number
        with patch("builtins.input", return_value="2"):
            result = get_valid_record_number(self.file_name, "Enter record number:")
            self.assertEqual(result, 2)
    
    def test_no_records(self):
        writer = csv.writer(self.temp_file)
        writer.writerow(["First Name", "Last Name", "Date of Birth"])
        self.temp_file.seek(0)

        # Test for no records available
        with patch("builtins.input", return_value="1"):  # Mock input
            with self.assertLogs(level="INFO") as log:  # Capture logs
                result = get_valid_record_number(self.file_name, "Enter record number:")
                self.assertIsNone(result)  # function returns None
                self.assertIn("ERROR:root:No records available.", log.output)

    def test_out_of_bounds_record_number(self):
        # Add sample data to the file
        writer = csv.writer(self.temp_file)
        writer.writerow(["First Name", "Last Name", "Date of Birth"])  # Header
        writer.writerow(["John", "Doe", "1990-01-01"])
        writer.writerow(["Jane", "Smith", "1985-05-15"])
        self.temp_file.seek(0)

        # Test for an out-of-bounds record number
        with patch("builtins.input", side_effect=["5", "1"]):
            with self.assertLogs(level="INFO") as log:
                result = get_valid_record_number(self.file_name, "Enter record number:")
                self.assertEqual(result, 1)
                self.assertIn("ERROR:root:Invalid record number. Please enter a record number between 1 and 2.", log.output)

class TestGetRecordLength(BaseTestCase):

    def test_valid_record_length(self):
        writer = csv.writer(self.temp_file)
        writer.writerow(["First Name", "Last Name", "Date of Birth"])  # Header
        writer.writerow(["John", "Doe", "1990-01-01"])
        writer.writerow(["Jane", "Smith", "1985-05-15"])
        writer.writerow(["Emily", "Davis", "2000-03-22"])
        self.temp_file.seek(0)

        # Test for a valid record length
        result = get_record_length(self.file_name)
        self.assertEqual(result, 3)

    def test_no_records(self):
        writer = csv.writer(self.temp_file)
        writer.writerow(["First Name", "Last Name", "Date of Birth"])
        self.temp_file.seek(0)

        with patch("builtins.input", return_value="1"):
            with self.assertLogs(level="INFO") as log: 
                result = get_valid_record_number(self.file_name, "Enter record number:")
                self.assertIsNone(result)
                self.assertIn("ERROR:root:No records available.", log.output)
