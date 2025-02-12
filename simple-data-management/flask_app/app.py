from flask import Flask, jsonify, render_template, redirect, url_for, flash, request
import requests

app = Flask(__name__)
app.secret_key = 'top_secret0'

API_BASE_URL = 'http://127.0.0.1:5000/api'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/records')
def view_records():
    try:
        response = requests.get(f'{API_BASE_URL}/records')
        response.raise_for_status()
        records = response.json().get('records', [])
    except requests.exceptions.RequestException as e:
        flash(f"An error occurred: {e}", "danger")
        records = []
    return render_template('records.html', records=records)

@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        form_data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'date_of_birth': request.form['dob']
        }
        try:
            response = requests.post(f'{API_BASE_URL}/create', json=form_data)
            response.raise_for_status()
            data = response.json()
            if data['success']:
                flash(data['message'], 'success')
                return redirect(url_for('view_records'))
            else:
                flash(data['errors'] or data['message'], 'danger')
        except requests.exceptions.RequestException as e:
            flash(f"An error occurred: {e}", "danger")
    return render_template('create.html')

@app.route('/delete', methods=['DELETE'])  
def delete():
    data = request.get_json()
    record_id = data.get('record_id')
    record_id = int(record_id)

    if not record_id:
        return jsonify({"success": False, "message": "Record ID is required"}), 400

    try:
        response = requests.delete(f'{API_BASE_URL}/delete', json={'record_id': record_id}) 
        response.raise_for_status()
        return jsonify(response.json())  # Return JSON response to frontend
    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "message": f"An error occurred: {e}"}), 500


@app.route('/update', methods=['POST'])
def update_record_route():
    form_data = {
        'record_id': request.form['record_id'],
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'date_of_birth': request.form['date_of_birth'],
    }

    try:
        response = requests.put(f'{API_BASE_URL}/update_record', json=form_data)
        response.raise_for_status()
        data = response.json()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # If this is an AJAX request, return JSON
            return jsonify(data)

        if data['success']:
            flash(data['message'], 'success')
            return redirect(url_for('view_records'))
        else:
            flash(data['errors'] or data['message'], 'danger')

    except requests.exceptions.RequestException as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({"success": False, "message": f"An error occurred: {e}"}), 500

        flash(f"An error occurred: {e}", "danger")

    return render_template('records.html')


if __name__ == '__main__':
    app.run(port=8000, debug=True)
