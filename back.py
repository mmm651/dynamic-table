from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

# Path to the Excel file
EXCEL_FILE = 'updated_data.xlsx'

# Route to serve the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to serve data from Excel
@app.route('/data')
def get_data():
    try:
        # Check if the Excel file exists
        if not os.path.exists(EXCEL_FILE):
            # Create a default file if it doesn't exist
            df = pd.DataFrame(columns=['Column1', 'Column2', 'Column3'])  # Default columns
            df.to_excel(EXCEL_FILE, index=False)

        # Load the Excel file
        data = pd.read_excel(EXCEL_FILE)

        # Replace NaN with None (valid in JSON)
        data = data.replace({np.nan: None})

        # Convert to JSON format
        return jsonify(data.to_dict(orient='records'))
    except Exception as e:
        # Handle exceptions and log errors
        app.logger.error(f"Error fetching data: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Route to save data to Excel
@app.route('/save', methods=['POST'])
def save_data():
    try:
        # Get JSON data from the request
        updated_data = request.json

        # Convert JSON to a pandas DataFrame
        df = pd.DataFrame(updated_data)

        # Save the DataFrame to the Excel file
        df.to_excel(EXCEL_FILE, index=False)

        return jsonify({"message": "Data saved successfully!"}), 200
    except Exception as e:
        # Handle exceptions
        app.logger.error(f"Error saving data: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
