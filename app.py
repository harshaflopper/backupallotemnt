from flask import Flask, render_template, jsonify, request, redirect, url_for
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static', static_url_path='')
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'faculty_json')
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_departments():
    """Get list of all department files"""
    departments = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.endswith('.json'):
            # Extract department name from filename (remove number and .json)
            name = ' '.join(filename.split('. ')[1:]).replace('.json', '').strip()
            departments.append({
                'id': filename,
                'name': name
            })
    return departments

def get_faculty(department_id):
    """Get faculty list for a department"""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], department_id)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_faculty(department_id, faculty_list):
    """Save faculty list for a department"""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], department_id)
    with open(filepath, 'w') as f:
        json.dump(faculty_list, f, indent=4)

@app.route('/')
def index():
    departments = get_departments()
    return render_template('index.html', departments=departments)

@app.route('/api/departments')
def api_departments():
    return jsonify(get_departments())

@app.route('/api/faculty/<path:department_id>')
def api_faculty(department_id):
    faculty = get_faculty(department_id)
    # Filter out inactive faculty (used by exam allotment)
    active_faculty = [f for f in faculty if f.get('isActive', True)]
    return jsonify(active_faculty)

@app.route('/api/faculty/<path:department_id>/all')
def api_faculty_all(department_id):
    """Get all faculty including inactive ones (used by faculty management page)"""
    faculty = get_faculty(department_id)
    return jsonify(faculty)

@app.route('/exam-allotment')
def exam_allotment():
    return render_template('exam_allotment.html')

@app.route('/api/faculty/<department_id>/add', methods=['POST'])
def add_faculty(department_id):
    try:
        # Get JSON data from request
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'No data provided'}), 400

        # Get existing faculty list
        faculty_list = get_faculty(department_id)
        
        # Create new faculty member with proper formatting
        new_faculty = {
            'Name': data.get('name', '').strip().title(),
            'Initials': data.get('initials', '').strip().upper(),
            'Designation': data.get('designation', '').strip(),
            'Phone': data.get('phone', '').strip(),
            'Email': data.get('email', '').strip().lower(),
            'isActive': True  # Initialize as active by default
        }

        # Validate required fields
        required_fields = ['Name', 'Initials', 'Designation', 'Phone', 'Email']
        for field in required_fields:
            if not new_faculty[field]:
                return jsonify({
                    'status': 'error',
                    'message': f'Missing required field: {field}'
                }), 400

        # Add to faculty list and save
        faculty_list.append(new_faculty)
        save_faculty(department_id, faculty_list)
        
        return jsonify({
            'status': 'success',
            'faculty': new_faculty
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/faculty/<department_id>/toggle_status', methods=['POST'])
def toggle_faculty_status(department_id):
    try:
        # Get the JSON data from the request
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'No data provided'}), 400
            
        faculty_index = data.get('index')
        if faculty_index is None:
            return jsonify({'status': 'error', 'message': 'Faculty index is required'}), 400
        
        # Convert index to integer if it's a string
        try:
            faculty_index = int(faculty_index)
        except (ValueError, TypeError):
            return jsonify({'status': 'error', 'message': 'Invalid faculty index'}), 400
            
        faculty_list = get_faculty(department_id)
        
        if 0 <= faculty_index < len(faculty_list):
            # Get the current status from the request if provided, otherwise toggle the existing one
            current_status = data.get('currentStatus')
            if current_status is None:
                current_status = faculty_list[faculty_index].get('isActive', True)
            
            # Toggle the status
            new_status = not current_status
            faculty_list[faculty_index]['isActive'] = new_status
            
            # Save the updated list
            save_faculty(department_id, faculty_list)
            
            # Return the new status
            return jsonify({
                'status': 'success', 
                'isActive': new_status,
                'message': 'Status updated successfully',
                'debug': {
                    'index': faculty_index,
                    'current_status': current_status,
                    'new_status': new_status
                }
            })
        
        return jsonify({
            'status': 'error', 
            'message': 'Faculty not found',
            'debug': {
                'index': faculty_index,
                'list_length': len(faculty_list)
            }
        }), 404
        
    except Exception as e:
        import traceback
        return jsonify({
            'status': 'error',
            'message': f'Failed to update status: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
