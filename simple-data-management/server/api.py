from flask import Flask, jsonify, request
from api.create import create_record
from api.retrieve import read_records
from api.update import update_record
from api.delete import delete_record
from flask_app.validation import validate_name, validate_dateOfBirth

app = Flask(__name__)
app.secret_key = 'top_secret0'

@app.route('/api/records', methods=['GET'])
def get_records():
    try:
        records, error = read_records()
        if error:
            return jsonify({'success': False, 'message': error}), 500

        print("Records from API:", records)
        return jsonify({'success': True, 'records': records}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/create', methods=['POST'])
def create_record_route():
    try:
        data = request.get_json()
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        date_of_birth = data.get('date_of_birth', '').strip()

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
        print(error)
        if error:
            return jsonify({"success": False, "message": f"Error: {error}"}), 500
        return jsonify({"success": True, "message": "Record successfully created!"}), 201
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": str(e)}), 501

@app.route('/api/delete', methods=['DELETE'])
def delete_record_route():
    print("Request body:", request.get_json())
    
    data = request.get_json()
    record_id = data.get('record_id')

    if record_id is None:
        return jsonify({"success": False, "message": "Record ID is required"}), 400

    error = delete_record(record_id)
    if error:
        return jsonify({"success": False, "message": f"Error: {error}"}), 500
    return jsonify({"success": True, "message": "Record successfully deleted!"}), 200


@app.route('/api/update_record', methods=['PUT'])
def api_update_record():
    try:
        data = request.get_json()
        
        # Ensure record_id is an integer
        record_id = int(data.get('record_id', 0))  
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        date_of_birth = data.get('date_of_birth', '').strip()

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
        print("Updating record with ID:", record_id) 
        error = update_record(record_id, first_name, last_name, date_of_birth)

        if error:
            print("Update Error:", error) 
            return jsonify({"success": False, "message": f"Error: {error}"}), 500

        return jsonify({"success": True, "message": "Record successfully updated!"}), 200

    except Exception as e:
        print("Unexpected Error:", e) 
        return jsonify({"success": False, "message": f"Unexpected error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)
