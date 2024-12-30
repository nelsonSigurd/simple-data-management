from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os
from datetime import datetime
from data_management import (
    validate_name, validate_dateOfBirth, create_record, delete_record,
    update_record as update_record_data, read_records)

app = Flask(__name__)
app.secret_key = 'top_secret0' 

CSV_FILE = 'people.csv'

# Ensure the CSV file exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["First Name", "Last Name", "Date of Birth"])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/records')
def view_records():
    records = []
    try:
        read_records(CSV_FILE)  # Your reusable function
        with open(CSV_FILE, mode='r') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip the header
            records = list(reader)
    except Exception as e:
        flash(f"An error occurred: {e}", "danger")
    return render_template('records.html', records=records)

@app.route('/create', methods=['GET', 'POST'])
def create():
    error_messages = []  # Collect validation errors
    if request.method == 'POST':
        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name'].strip()
        date_of_birth = request.form['date_of_birth'].strip()

        # Validate Name Fields
        valid_first, error_first = validate_name(first_name)
        if not valid_first:
            error_messages.append(f"First Name: {error_first}")
        
        valid_last, error_last = validate_name(last_name)
        if not valid_last:
            error_messages.append(f"Last Name: {error_last}")

        # Validate Date of Birth
        valid_dob, error_dob = validate_dateOfBirth(date_of_birth)
        if not valid_dob:
            error_messages.append(f"Date of Birth: {error_dob}")

        # Check if there are validation errors
        if error_messages:
            return render_template('create.html', errors=error_messages)
        
        # If all inputs are valid, create the record
        error = create_record(CSV_FILE, first_name, last_name, date_of_birth)
        if error:
            flash(f"Error: {error}", "danger")
        else:
            flash("Record successfully created!", "success")
            return redirect(url_for('view_records'))

    return render_template('create.html', errors=[])

@app.route('/delete', methods=['POST'])
def delete():
    record_id = int(request.form['record_id'])
    try:
        delete_record(CSV_FILE, record_id)  # 
        flash("Record successfully deleted!", "success")
    except Exception as e:
        flash(f"An error occurred: {e}", "danger")
    return redirect(url_for('view_records'))

@app.route('/update', methods=['POST'])
def update_record_route():
    record_id = int(request.form['record_id'])  # From form hidden input
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    date_of_birth = request.form['date_of_birth']

    # Input validation using existing functions
    is_valid_name, name_error = validate_name(first_name)
    if not is_valid_name:
        flash(name_error, 'danger')
        return redirect(url_for('view_records'))

    is_valid_last_name, last_name_error = validate_name(last_name)
    if not is_valid_last_name:
        flash(last_name_error, 'danger')
        return redirect(url_for('view_records'))

    is_valid_date, date_error = validate_dateOfBirth(date_of_birth)
    if not is_valid_date:
        flash(date_error, 'danger')
        return redirect(url_for('view_records'))

    # Call the correct update_record function
    try:
        error = update_record_data(CSV_FILE, record_id, first_name, last_name, date_of_birth)
        if error:
            flash(error, 'danger')  # Show error if the function returns one
        else:
            flash("Record successfully updated!", "success")
    except Exception as e:
        flash(f"An error occurred: {e}", "danger")

    return redirect(url_for('view_records'))

if __name__ == '__main__':
    app.run(debug=True)