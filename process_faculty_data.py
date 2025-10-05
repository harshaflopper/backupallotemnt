import json
import os

def process_faculty_data():
    # Create the faculty_json directory if it doesn't exist
    os.makedirs('faculty_json', exist_ok=True)
    
    # Sample data structure to hold departments and their faculty
    departments = {
        'ARCH': {
            'id': 1,
            'name': 'ARCH',
            'faculty': []
        },
        'IT ELECTRONICS AND INSTRUMENTATION': {
            'id': 2,
            'name': 'IT ELECTRONICS AND INSTRUMENTATION',
            'faculty': []
        },
        'MBA': {
            'id': 3,
            'name': 'MBA',
            'faculty': []
        },
        'MECHANICAL ENGINEERING': {
            'id': 4,
            'name': 'MECHANICAL ENGINEERING',
            'faculty': []
        },
        'TELECOMMUNICATION AND ENGINEERING': {
            'id': 5,
            'name': 'TELECOMMUNICATION AND ENGINEERING',
            'faculty': []
        },
        'NANO TECHNOLOGY': {
            'id': 6,
            'name': 'NANO TECHNOLOGY',
            'faculty': []
        },
        'BIO-TECHNOLOGY': {
            'id': 7,
            'name': 'BIO-TECHNOLOGY',
            'faculty': []
        },
        'CHEMICAL ENGINEERING': {
            'id': 8,
            'name': 'CHEMICAL ENGINEERING',
            'faculty': []
        },
        'CIVIL ENGINEERING': {
            'id': 9,
            'name': 'CIVIL ENGINEERING',
            'faculty': []
        },
        'COMPUTER SCIENCE AND ENGINEERING': {
            'id': 10,
            'name': 'COMPUTER SCIENCE AND ENGINEERING',
            'faculty': []
        },
        'EEE ELECTRICAL ENGINEERING': {
            'id': 11,
            'name': 'EEE ELECTRICAL ENGINEERING',
            'faculty': []
        },
        'ECE ELECTRONICS AND COMMUNICATION ENGINEERING': {
            'id': 12,
            'name': 'ECE ELECTRONICS AND COMMUNICATION ENGINEERING',
            'faculty': []
        },
        'INDUSTRIAL ENGINEERING AND MANAGEMENT': {
            'id': 13,
            'name': 'INDUSTRIAL ENGINEERING AND MANAGEMENT',
            'faculty': []
        },
        'INFORMATION SCIENCE AND ENGINEERING': {
            'id': 14,
            'name': 'INFORMATION SCIENCE AND ENGINEERING',
            'faculty': []
        }
    }
    
    # Sample faculty data (you'll replace this with your actual data)
    faculty_data = """
    1,Dr. Madhumathi P,Professor,ARCH,9916071151,madhumathi@sit.ac.in
    2,Siddeshagowda S,Assistant Professor,ARCH,7022715643,siddu.art@sit.ac.in
    3,Bhoomika U,Assistant Professor,ARCH,9902829404,bhoomikau@sit.ac.in
    """
    
    # Process the faculty data
    for line in faculty_data.strip().split('\n'):
        if not line.strip():
            continue
            
        try:
            # Parse the line (adjust the parsing logic based on your actual data format)
            parts = [p.strip() for p in line.split(',')]
            if len(parts) >= 6:
                faculty = {
                    'Name': parts[1],
                    'Designation': parts[2],
                    'Phone': parts[4],
                    'Email': parts[5],
                    'isActive': True
                }
                
                # Add to the appropriate department
                dept_name = parts[3]
                if dept_name in departments:
                    departments[dept_name]['faculty'].append(faculty)
                else:
                    print(f"Warning: Department '{dept_name}' not found in departments list")
                    
        except Exception as e:
            print(f"Error processing line: {line}")
            print(f"Error: {str(e)}")
    
    # Save each department's faculty to a separate JSON file
    for dept_name, dept_data in departments.items():
        if dept_data['faculty']:  # Only create file if there are faculty members
            filename = f"{dept_data['id']}. {dept_name}.json"
            filepath = os.path.join('faculty_json', filename.replace('/', '_'))
            
            with open(filepath, 'w') as f:
                json.dump(dept_data['faculty'], f, indent=2)
            
            print(f"Saved {len(dept_data['faculty'])} faculty members to {filename}")
    
    # Also create a departments.json file
    dept_list = [
        {'id': dept['id'], 'name': dept['name']} 
        for dept in departments.values()
    ]
    
    with open('faculty_json/departments.json', 'w') as f:
        json.dump(dept_list, f, indent=2)
    
    print("\nDepartments and faculty data processed successfully!")

if __name__ == '__main__':
    process_faculty_data()
