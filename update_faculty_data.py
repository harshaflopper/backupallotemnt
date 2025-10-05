import json
import os

def update_faculty_data():
    # Create the faculty_json directory if it doesn't exist
    os.makedirs('faculty_json', exist_ok=True)
    
    # Department mapping with their IDs
    departments = {
        'ARCH': {
            'id': 1,
            'name': 'ARCHITECTURE',
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
            'name': 'ELECTRICAL AND ELECTRONICS ENGINEERING',
            'faculty': []
        },
        'ECE ELECTRONICS AND COMMUNICATION ENGINEERING': {
            'id': 12,
            'name': 'ELECTRONICS AND COMMUNICATION ENGINEERING',
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

    # Sample faculty data (you can add more faculty here)
    faculty_data = """
    Dr. Madhumathi P,Professor,ARCH,9916071151,madhumathi@sit.ac.in
    Siddeshagowda S,Assistant Professor,ARCH,7022715643,siddu.art@sit.ac.in
    Bhoomika U,Assistant Professor,ARCH,9902829404,bhoomikau@sit.ac.in
    Gautham N,Assistant Professor,ARCH,9538402926,gautham@sit.ac.in
    Vijetha C P,Assistant Professor,ARCH,9986752725,vijethacp@sit.ac.in
    Mohamed Inam Ulla Khan,Assistant Professor,ARCH,8105221190,mdinamuk@sit.ac.in
    """

    # Process faculty data
    for line in faculty_data.strip().split('\n'):
        if not line.strip():
            continue
            
        try:
            parts = [p.strip() for p in line.split(',')]
            if len(parts) >= 5:
                faculty = {
                    'Name': parts[0],
                    'Designation': parts[1],
                    'Phone': parts[3],
                    'Email': parts[4],
                    'isActive': True
                }
                
                dept_code = parts[2]
                if dept_code in departments:
                    departments[dept_code]['faculty'].append(faculty)
                else:
                    print(f"Warning: Department code '{dept_code}' not found")
                    
        except Exception as e:
            print(f"Error processing line: {line}")
            print(f"Error: {str(e)}")
    
    # Save each department's faculty to a separate JSON file
    for dept_code, dept_data in departments.items():
        if dept_data['faculty']:
            filename = f"{dept_data['id']}. {dept_data['name']}.json"
            filepath = os.path.join('faculty_json', filename.replace('/', '_'))
            
            with open(filepath, 'w') as f:
                json.dump(dept_data['faculty'], f, indent=2)
            
            print(f"Saved {len(dept_data['faculty'])} faculty members to {filename}")
    
    # Update departments.json
    dept_list = [
        {'id': dept['id'], 'name': dept['name']} 
        for dept in departments.values()
    ]
    
    with open('faculty_json/departments.json', 'w') as f:
        json.dump(dept_list, f, indent=2)
    
    print("\nFaculty data updated successfully!")

if __name__ == '__main__':
    update_faculty_data()
