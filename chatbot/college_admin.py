"""
College Administration Interface

This module provides functionality to add, edit, and manage colleges in the database.
It includes validation, data formatting, and easy-to-use functions for administrators.
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime

def add_college_to_database(college_data: Dict) -> bool:
    """
    Add a new college to the database
    
    Args:
        college_data: Dictionary containing college information
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Validate required fields
        required_fields = ['name', 'location', 'type', 'founded', 'ranking', 'acceptance_rate']
        for field in required_fields:
            if field not in college_data:
                print(f"Error: Missing required field '{field}'")
                return False
        
        # Validate data types
        if not isinstance(college_data['ranking'], int):
            print("Error: Ranking must be an integer")
            return False
        
        if not isinstance(college_data['acceptance_rate'], (int, float)):
            print("Error: Acceptance rate must be a number")
            return False
        
        if not isinstance(college_data['founded'], int):
            print("Error: Founded year must be an integer")
            return False
        
        # Generate college key from name
        college_key = college_data['name'].lower().replace(' ', '').replace('university', '').replace('college', '')
        
        # Load existing data
        from college_data import COLLEGES_DATA
        
        # Check if college already exists
        if college_key in COLLEGES_DATA:
            print(f"Error: College '{college_data['name']}' already exists")
            return False
        
        # Add to database
        COLLEGES_DATA[college_key] = college_data
        
        # Save to file (optional - for persistence)
        save_colleges_to_file()
        
        print(f"Successfully added {college_data['name']} to the database!")
        return True
        
    except Exception as e:
        print(f"Error adding college: {e}")
        return False

def create_college_template() -> Dict:
    """
    Create a template for adding a new college
    
    Returns:
        Dict: Template with all required fields
    """
    return {
        "name": "University Name",
        "location": "City, State",
        "type": "Private/Public Research University",
        "founded": 1900,
        "ranking": 1,
        "acceptance_rate": 10.0,
        "tuition": {
            "undergraduate": 50000,
            "graduate": 50000,
            "room_board": 15000
        },
        "programs": {
            "undergraduate": [
                "Program 1", "Program 2", "Program 3"
            ],
            "graduate": [
                "Graduate Program 1", "Graduate Program 2"
            ]
        },
        "admission_requirements": {
            "gpa": 3.5,
            "sat_score": 1400,
            "act_score": 32,
            "toefl": 80,
            "ielts": 6.5,
            "essays": 2,
            "recommendations": 2,
            "deadline": "January 1"
        },
        "campus_life": {
            "student_population": 10000,
            "undergraduate": 5000,
            "graduate": 5000,
            "international_students": 15,
            "student_faculty_ratio": 10,
            "housing": "Available"
        },
        "notable_features": [
            "Feature 1", "Feature 2", "Feature 3"
        ],
        "website": "https://www.university.edu",
        "contact": {
            "phone": "(555) 123-4567",
            "email": "admissions@university.edu"
        }
    }

def validate_college_data(college_data: Dict) -> List[str]:
    """
    Validate college data and return list of errors
    
    Args:
        college_data: Dictionary containing college information
        
    Returns:
        List[str]: List of validation errors
    """
    errors = []
    
    # Required fields
    required_fields = ['name', 'location', 'type', 'founded', 'ranking', 'acceptance_rate']
    for field in required_fields:
        if field not in college_data:
            errors.append(f"Missing required field: {field}")
    
    # Data type validations
    if 'ranking' in college_data and not isinstance(college_data['ranking'], int):
        errors.append("Ranking must be an integer")
    
    if 'acceptance_rate' in college_data and not isinstance(college_data['acceptance_rate'], (int, float)):
        errors.append("Acceptance rate must be a number")
    
    if 'founded' in college_data and not isinstance(college_data['founded'], int):
        errors.append("Founded year must be an integer")
    
    # Range validations
    if 'acceptance_rate' in college_data and (college_data['acceptance_rate'] < 0 or college_data['acceptance_rate'] > 100):
        errors.append("Acceptance rate must be between 0 and 100")
    
    if 'ranking' in college_data and college_data['ranking'] < 1:
        errors.append("Ranking must be a positive integer")
    
    if 'founded' in college_data and (college_data['founded'] < 1000 or college_data['founded'] > datetime.now().year):
        errors.append("Founded year must be between 1000 and current year")
    
    return errors

def save_colleges_to_file():
    """Save colleges data to a JSON file for persistence"""
    try:
        from college_data import COLLEGES_DATA
        with open('colleges_backup.json', 'w') as f:
            json.dump(COLLEGES_DATA, f, indent=2)
        print("Colleges data saved to colleges_backup.json")
    except Exception as e:
        print(f"Error saving colleges data: {e}")

def load_colleges_from_file():
    """Load colleges data from JSON file"""
    try:
        if os.path.exists('colleges_backup.json'):
            with open('colleges_backup.json', 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Error loading colleges data: {e}")
        return {}

def list_all_colleges() -> List[Dict]:
    """Get list of all colleges with basic information"""
    from college_data import COLLEGES_DATA
    colleges = []
    for key, college in COLLEGES_DATA.items():
        colleges.append({
            'key': key,
            'name': college['name'],
            'location': college['location'],
            'ranking': college['ranking'],
            'acceptance_rate': college['acceptance_rate']
        })
    return sorted(colleges, key=lambda x: x['ranking'])

def search_colleges_by_criteria(criteria: Dict) -> List[Dict]:
    """
    Search colleges by various criteria
    
    Args:
        criteria: Dictionary with search criteria
        
    Returns:
        List[Dict]: Matching colleges
    """
    from college_data import COLLEGES_DATA
    results = []
    
    for key, college in COLLEGES_DATA.items():
        match = True
        
        # Search by ranking range
        if 'min_ranking' in criteria and college['ranking'] > criteria['min_ranking']:
            match = False
        if 'max_ranking' in criteria and college['ranking'] < criteria['max_ranking']:
            match = False
        
        # Search by acceptance rate range
        if 'min_acceptance_rate' in criteria and college['acceptance_rate'] < criteria['min_acceptance_rate']:
            match = False
        if 'max_acceptance_rate' in criteria and college['acceptance_rate'] > criteria['max_acceptance_rate']:
            match = False
        
        # Search by location
        if 'location' in criteria and criteria['location'].lower() not in college['location'].lower():
            match = False
        
        # Search by type
        if 'type' in criteria and criteria['type'].lower() not in college['type'].lower():
            match = False
        
        if match:
            results.append(college)
    
    return sorted(results, key=lambda x: x['ranking'])

def get_college_statistics() -> Dict:
    """Get statistics about the college database"""
    from college_data import COLLEGES_DATA
    
    if not COLLEGES_DATA:
        return {"error": "No colleges in database"}
    
    colleges = list(COLLEGES_DATA.values())
    
    stats = {
        "total_colleges": len(colleges),
        "average_acceptance_rate": sum(c['acceptance_rate'] for c in colleges) / len(colleges),
        "average_tuition": sum(c['tuition']['undergraduate'] for c in colleges) / len(colleges),
        "rankings_range": {
            "min": min(c['ranking'] for c in colleges),
            "max": max(c['ranking'] for c in colleges)
        },
        "colleges_by_type": {},
        "colleges_by_state": {}
    }
    
    # Count by type
    for college in colleges:
        college_type = college['type']
        stats['colleges_by_type'][college_type] = stats['colleges_by_type'].get(college_type, 0) + 1
    
    # Count by state
    for college in colleges:
        state = college['location'].split(',')[-1].strip()
        stats['colleges_by_state'][state] = stats['colleges_by_state'].get(state, 0) + 1
    
    return stats

# Example usage and testing
if __name__ == "__main__":
    print("College Administration Interface")
    print("=" * 40)
    
    # Show current statistics
    stats = get_college_statistics()
    print(f"Total colleges: {stats['total_colleges']}")
    print(f"Average acceptance rate: {stats['average_acceptance_rate']:.1f}%")
    print(f"Average tuition: ${stats['average_tuition']:,.0f}")
    
    # Show template
    print("\nCollege Template:")
    template = create_college_template()
    print(json.dumps(template, indent=2))
    
    # Example of adding a new college
    print("\nExample: Adding a new college...")
    new_college = {
        "name": "Example University",
        "location": "Example City, State",
        "type": "Private Research University",
        "founded": 1950,
        "ranking": 16,
        "acceptance_rate": 15.0,
        "tuition": {
            "undergraduate": 45000,
            "graduate": 45000,
            "room_board": 12000
        },
        "programs": {
            "undergraduate": ["Computer Science", "Engineering", "Business"],
            "graduate": ["MBA", "MS Computer Science"]
        },
        "admission_requirements": {
            "gpa": 3.5,
            "sat_score": 1400,
            "act_score": 32,
            "toefl": 80,
            "ielts": 6.5,
            "essays": 2,
            "recommendations": 2,
            "deadline": "January 15"
        },
        "campus_life": {
            "student_population": 8000,
            "undergraduate": 5000,
            "graduate": 3000,
            "international_students": 20,
            "student_faculty_ratio": 12,
            "housing": "Available"
        },
        "notable_features": [
            "Strong research programs",
            "Beautiful campus",
            "Diverse student body"
        ],
        "website": "https://www.example.edu",
        "contact": {
            "phone": "(555) 123-4567",
            "email": "admissions@example.edu"
        }
    }
    
    # Validate the data
    errors = validate_college_data(new_college)
    if errors:
        print("Validation errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("Data validation passed!")
        # Uncomment to actually add the college
        # add_college_to_database(new_college)
