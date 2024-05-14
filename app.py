from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
from datetime import datetime
import pandas as pd

app = Flask(__name__)

# Define function to fetch data from database
def fetch_data():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM entries")
    data = c.fetchall()
    conn.close()
    return data

@app.route('/integration')
def index():
    associate_name = request.args.get('associate_name', '')  # Get associate_name from query parameters
    # Fetch data from database
    data = fetch_data()
    return render_template('index.html', associate_name=associate_name, data=data)


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == "POST":
        associate_name = request.form['associate_name']
        module_serial = request.form['module_serial']
        mbo_serial = request.form['mbo_serial']
        control_card_serial = request.form['control_card_serial']
        result = "pass"
        print(associate_name, module_serial, mbo_serial, control_card_serial)
        # Check if module serial, MBO serial, and control card serial match
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('''INSERT INTO entries (associate_name, module_serial, mbo_serial, control_card_serial, result, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)''', (associate_name, module_serial, mbo_serial, control_card_serial, result, str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
        conn.commit()
        conn.close()
        return redirect(url_for('index', associate_name=associate_name))

@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
        # Fetch data from database
        data = fetch_data()
        # Convert data to DataFrame
        df = pd.DataFrame(data, columns=['ID', 'Associate Name', 'Module Serial', 'MBO Serial', 'Control Card Serial', 'Result', 'Timestamp'])
        # Generate Excel file
        excel_file = 'data.xlsx'
        df.to_excel(excel_file, index=False)
        # Serve the Excel file for download
        return send_file(excel_file, as_attachment=True)
    else:
        # Fetch data from database
        data = fetch_data()
        print(data)
        return render_template('download.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
