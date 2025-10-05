import os
import json

def update_faculty_status(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r+', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                        updated = False
                        
                        # Handle both array and object formats
                        if isinstance(data, list):
                            for faculty in data:
                                if isinstance(faculty, dict) and 'isActive' not in faculty:
                                    faculty['isActive'] = True
                                    updated = True
                        elif isinstance(data, dict):
                            # If the file has faculty as a nested list under a key
                            for key, value in data.items():
                                if isinstance(value, list):
                                    for faculty in value:
                                        if isinstance(faculty, dict) and 'isActive' not in faculty:
                                            faculty['isActive'] = True
                                            updated = True
                        
                        if updated:
                            f.seek(0)
                            json.dump(data, f, indent=4, ensure_ascii=False)
                            f.truncate()
                            print(f"Updated {filename}")
                        else:
                            print(f"No updates needed for {filename}")
                            
                    except json.JSONDecodeError as e:
                        print(f"Error parsing {filename}: {e}")
                        
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    faculty_dir = os.path.join(os.path.dirname(__file__), 'faculty_json')
    update_faculty_status(faculty_dir)
    print("Update complete!")
