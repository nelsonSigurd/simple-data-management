from flask import Flask, render_template, redirect, url_for, flash, request
import requests

app = Flask(__name__)
app.secret_key = 'top_secret0'

API_BASE_URL = 'http://127.0.0.1:500'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/records')
def view_records():
    try:
        response = requests.get(f'{API_BASE_URL}/records')
        response.raise_for_status()
        records = response.json()
    except requests.exceptions.RequestException as e:
        flash(f"An error occurred: {e}", "danger")
        records = []
    return render_template('records.html', records=records)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        form_data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'date_of_birth': request.form['dob']
        }
        try:
            response = requests.post(f'{API_BASE_URL}/create', data=form_data)
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

@app.route('/delete', methods=['POST'])
def delete():
    record_id = request.form.get('record_id')
    try:
        response = requests.post(f'{API_BASE_URL}/delete', data={'record_id': record_id})
        response.raise_for_status()
        data = response.json()
        if data['success']:
            flash(data['message'], 'success')
        else:
            flash(data['message'], 'danger')
    except requests.exceptions.RequestException as e:
        flash(f"An error occurred: {e}", "danger")
    return redirect(url_for('view_records'))

@app.route('/update', methods=['GET', 'POST'])
def update_record_route():
    if request.method == 'POST':
        form_data = {
            'record_id': request.form['record_id'],
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'date_of_birth': request.form['dob']
        }
        try:
            response = requests.put(f'{API_BASE_URL}/update_record', data=form_data)
            response.raise_for_status()
            data = response.json()
            if data['success']:
                flash(data['message'], 'success')
                return redirect(url_for('view_records'))
            else:
                flash(data['errors'] or data['message'], 'danger')
        except requests.exceptions.RequestException as e:
            flash(f"An error occurred: {e}", "danger")
    return render_template('update.html')

if __name__ == '__main__':
    app.run(port=8000, debug=True)
