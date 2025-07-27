from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_excel():
    file = request.files.get('file')

    if not file:
        return jsonify({"error": "No file received!"})

    if not file.filename.endswith('.xlsx'):
        return jsonify({"error": "Only .xlsx files are supported"})

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        df = pd.read_excel(filepath)

        # Validate required columns
        if 'Total' not in df.columns or 'Student Name' not in df.columns:
            return jsonify({"error": "Excel file must contain 'Total' and 'Student Name' columns."})

        topper = df.loc[df['Total'].idxmax()]['Student Name']
        average = df['Total'].mean()

        return jsonify({"topper": topper, "average": round(average, 2)})
    except Exception as e:
        return jsonify({"error": f"Failed to process file: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)