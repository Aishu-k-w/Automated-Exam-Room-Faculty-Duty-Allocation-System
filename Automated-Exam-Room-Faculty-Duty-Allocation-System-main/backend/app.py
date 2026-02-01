from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import os
import pandas as pd
from allocation import allocate_students_to_classrooms, allocate_faculty_to_classrooms
import re

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/phase2.html')
def phase2():
    return send_from_directory(app.static_folder, 'phase2.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Get form data
        num_students = int(request.form.get('num_students'))
        start_usn = request.form.get('start_usn')
        
        # Handle file upload
        if 'classroom_file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
            
        file = request.files['classroom_file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
            
        if not file.filename.endswith('.xlsx'):
            return jsonify({'error': 'Please upload an Excel file'}), 400
            
        # Save uploaded file
        filepath = os.path.join(UPLOAD_FOLDER, 'classrooms.xlsx')
        file.save(filepath)
        
        # Process allocation
        result_df = allocate_students_to_classrooms(num_students, start_usn, filepath)
        
        # Save result
        result_path = os.path.join(RESULT_FOLDER, 'classroom_allocation.xlsx')
        result_df.to_excel(result_path, index=False)
        
        return jsonify({
            'message': 'Allocation completed successfully',
            'result_file': 'classroom_allocation.xlsx'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/allocate', methods=['POST'])
def allocate():
    try:
        # Only require exam and faculty timetable files
        if 'exam_timetable_file' not in request.files or \
           'faculty_timetable_file' not in request.files:
            return jsonify({'error': 'Both exam and faculty timetable files are required'}), 400

        exam_timetable_file = request.files['exam_timetable_file']
        faculty_timetable_file = request.files['faculty_timetable_file']

        et_path = os.path.join(UPLOAD_FOLDER, 'exam_timetable.xlsx')
        ft_path = os.path.join(UPLOAD_FOLDER, 'faculty_timetable.xlsx')
        exam_timetable_file.save(et_path)
        faculty_timetable_file.save(ft_path)

        # Use the latest classroom allocation from Phase 1
        ca_path = os.path.join(RESULT_FOLDER, 'classroom_allocation.xlsx')
        if not os.path.exists(ca_path):
            return jsonify({'error': 'Classroom allocation from Phase 1 not found. Please complete Phase 1 first.'}), 400

        # Process allocation
        result_df = allocate_faculty_to_classrooms(ca_path, et_path, ft_path)
        result_path = os.path.join(RESULT_FOLDER, 'faculty_allocation.xlsx')
        result_df.to_excel(result_path, index=False)
        return jsonify({'message': 'Faculty allocation completed', 'result_file': 'faculty_allocation.xlsx'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/phase1', methods=['GET'])
def download_phase1():
    try:
        result_path = os.path.join(RESULT_FOLDER, 'classroom_allocation.xlsx')
        if not os.path.exists(result_path):
            return jsonify({'error': 'Result file not found'}), 404
        return send_file(result_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/phase2', methods=['GET'])
def download_phase2():
    try:
        result_path = os.path.join(RESULT_FOLDER, 'faculty_allocation.xlsx')
        if not os.path.exists(result_path):
            return jsonify({'error': 'Result file not found'}), 404
        return send_file(result_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def extract_usn_parts(usn):
    """Extract prefix and numeric part from USN."""
    match = re.match(r'^(.*?)(\\d+)$', usn)
    if match:
        prefix, number = match.groups()
        return prefix, int(number)
    raise ValueError("Invalid USN format")

def generate_next_usn(current_usn, increment=1):
    """Generate next USN by incrementing the numeric part."""
    prefix, numeric_part = extract_usn_parts(current_usn)
    return f"{prefix}{numeric_part + increment:03d}"

if __name__ == '__main__':
    app.run(debug=True) 