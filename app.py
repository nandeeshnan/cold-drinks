from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Set folder for storing Excel files
EXCEL_DIR = os.path.expanduser('~/Desktop/excel_files')  # Folder where Excel files will be saved
os.makedirs(EXCEL_DIR, exist_ok=True)  # Create the directory if it doesn't exist

# Function to get today's Excel file name
def get_excel_file_name():
    today = datetime.now().strftime("%Y-%m-%d")  # e.g., 2024-12-04
    return os.path.join(EXCEL_DIR, f"data_{today}.xlsx")

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Get user input from the form
    date = request.form.get('date')
    name = request.form.get('name')
    outlet = request.form.get('outlet')
    comments = request.form.get('comments')

    # Prepare today's Excel file
    excel_file = get_excel_file_name()

    # If file doesn't exist, create a new one with headers
    if not os.path.exists(excel_file):
        df = pd.DataFrame(columns=["Date", "Name", "Outlet", "Comments"])
        df.to_excel(excel_file, index=False)

    # Append new data to today's Excel file
    new_data = pd.DataFrame([{"Date": date, "Name": name, "Outlet": outlet, "Comments": comments}])
    df = pd.read_excel(excel_file)
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_excel(excel_file, index=False)

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
