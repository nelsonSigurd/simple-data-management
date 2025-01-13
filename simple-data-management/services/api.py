from flask import Flask, jsonify, request
from flask_app.data_management import (create_record, delete_record, update_record as update_record_data, read_records)
from flask_app.validation import (validate_name, validate_dateOfBirth)

app = Flask(__name__)
app.secret_key = 'top_secret0'

@app.route('/records', methods=['GET'])
def get_records():
    try:
        records, error = read_records()
        if error:
            return jsonify({'success': False, 'message': error}), 500
        
        print("Records from API:", records)  # Add this line to print the records
        return jsonify(records), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/create', methods=['POST'])
def create_record_route():
    try:
        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name'].strip()
        date_of_birth = request.form['date_of_birth'].strip()

        # Validate input
        error_messages = []
        valid_first, error_first = validate_name(first_name)
        if not valid_first:
            error_messages.append(f"First Name: {error_first}")
        
        valid_last, error_last = validate_name(last_name)
        if not valid_last:
            error_messages.append(f"Last Name: {error_last}")

        valid_dob, error_dob = validate_dateOfBirth(date_of_birth)
        if not valid_dob:
            error_messages.append(f"Date of Birth: {error_dob}")

        if error_messages:
            return jsonify({"success": False, "errors": error_messages}), 400

        # Create record
        error = create_record(first_name, last_name, date_of_birth)
        if error:
            return jsonify({"success": False, "message": f"Error: {error}"}), 500
        return jsonify({"success": True, "message": "Record successfully created!"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/delete', methods=['POST'])
def delete_record_route():
    record_id = request.form.get('record_id', type=int)
    if record_id is None:
        return jsonify({"success": False, "message": "Record ID is required"}), 400

    error = delete_record(record_id)
    if error:
        return jsonify({"success": False, "message": f"Error: {error}"}), 500
    return jsonify({"success": True, "message": "Record successfully deleted!"}), 200

@app.route('/update_record', methods=['PUT'])
def api_update_record():
    record_id = request.form.get('record_id', type=int)
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    date_of_birth = request.form['date_of_birth']

    # Validate input
    error_messages = []
    valid_first, error_first = validate_name(first_name)
    if not valid_first:
        error_messages.append(f"First Name: {error_first}")
    
    valid_last, error_last = validate_name(last_name)
    if not valid_last:
        error_messages.append(f"Last Name: {error_last}")

    valid_dob, error_dob = validate_dateOfBirth(date_of_birth)
    if not valid_dob:
        error_messages.append(f"Date of Birth: {error_dob}")

    if error_messages:
        return jsonify({"success": False, "errors": error_messages}), 400

    # Update record
    error = update_record_data(record_id, first_name, last_name, date_of_birth)
    if error:
        return jsonify({"success": False, "message": f"Error: {error}"}), 500
    return jsonify({"success": True, "message": "Record successfully updated!"}), 200

if __name__ == '__main__':
    app.run(port=500, debug=True)