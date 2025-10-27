"""
College Information Database

This module contains comprehensive information about various colleges including
programs, admission requirements, fees, rankings, and other relevant details.
"""

from typing import Dict, List, Optional
import json

# Comprehensive college database
COLLEGES_DATA = {
    "harvard": {
        "name": "Harvard University",
        "location": "Cambridge, Massachusetts",
        "type": "Private Research University",
        "founded": 1636,
        "ranking": 1,
        "acceptance_rate": 3.4,
        "tuition": {
            "undergraduate": 57261,
            "graduate": 52000,
            "room_board": 18000
        },
        "programs": {
            "undergraduate": [
                "Computer Science", "Economics", "Psychology", "Biology", "Political Science",
                "English", "History", "Mathematics", "Physics", "Chemistry", "Engineering"
            ],
            "graduate": [
                "MBA", "Law", "Medicine", "Public Health", "Education", "Engineering",
                "Arts and Sciences", "Divinity", "Design", "Government"
            ]
        },
        "admission_requirements": {
            "gpa": 3.9,
            "sat_score": 1520,
            "act_score": 34,
            "toefl": 100,
            "ielts": 7.0,
            "essays": 2,
            "recommendations": 2,
            "deadline": "January 1"
        },
        "campus_life": {
            "student_population": 23000,
            "undergraduate": 6700,
            "graduate": 16300,
            "international_students": 25,
            "student_faculty_ratio": 6,
            "housing": "Guaranteed for 4 years"
        },
        "notable_features": [
            "Ivy League member",
            "World's largest academic library system",
            "Nobel Prize winners among faculty",
            "Strong alumni network",
            "Research opportunities"
        ],
        "website": "https://www.harvard.edu",
        "contact": {
            "phone": "(617) 495-1000",
            "email": "college@harvard.edu"
        }
    },
    
    "mit": {
        "name": "Massachusetts Institute of Technology",
        "location": "Cambridge, Massachusetts",
        "type": "Private Research University",
        "founded": 1861,
        "ranking": 2,
        "acceptance_rate": 6.7,
        "tuition": {
            "undergraduate": 57986,
            "graduate": 57986,
            "room_board": 17000
        },
        "programs": {
            "undergraduate": [
                "Computer Science", "Electrical Engineering", "Mechanical Engineering",
                "Physics", "Mathematics", "Biology", "Chemistry", "Economics",
                "Architecture", "Urban Planning", "Materials Science"
            ],
            "graduate": [
                "Engineering", "Science", "Architecture", "Management", "Urban Studies",
                "Media Arts", "Computational Science", "Technology Policy"
            ]
        },
        "admission_requirements": {
            "gpa": 3.9,
            "sat_score": 1540,
            "act_score": 35,
            "toefl": 90,
            "ielts": 7.0,
            "essays": 2,
            "recommendations": 2,
            "deadline": "January 1"
        },
        "campus_life": {
            "student_population": 12000,
            "undergraduate": 4600,
            "graduate": 7400,
            "international_students": 33,
            "student_faculty_ratio": 3,
            "housing": "Guaranteed for 4 years"
        },
        "notable_features": [
            "World leader in STEM education",
            "Strong entrepreneurship culture",
            "Cutting-edge research facilities",
            "Innovation and technology focus",
            "Collaborative learning environment"
        ],
        "website": "https://www.mit.edu",
        "contact": {
            "phone": "(617) 253-1000",
            "email": "admissions@mit.edu"
        }
    },
    
    "stanford": {
        "name": "Stanford University",
        "location": "Stanford, California",
        "type": "Private Research University",
        "founded": 1885,
        "ranking": 3,
        "acceptance_rate": 4.3,
        "tuition": {
            "undergraduate": 61731,
            "graduate": 61731,
            "room_board": 19000
        },
        "programs": {
            "undergraduate": [
                "Computer Science", "Engineering", "Biology", "Psychology", "Economics",
                "Political Science", "English", "History", "Mathematics", "Physics",
                "Chemistry", "Art", "Music", "Theater"
            ],
            "graduate": [
                "Business", "Law", "Medicine", "Education", "Engineering", "Humanities",
                "Sciences", "Earth Sciences", "Public Policy"
            ]
        },
        "admission_requirements": {
            "gpa": 3.9,
            "sat_score": 1505,
            "act_score": 34,
            "toefl": 100,
            "ielts": 7.0,
            "essays": 3,
            "recommendations": 2,
            "deadline": "January 2"
        },
        "campus_life": {
            "student_population": 17000,
            "undergraduate": 7000,
            "graduate": 10000,
            "international_students": 23,
            "student_faculty_ratio": 5,
            "housing": "Guaranteed for 4 years"
        },
        "notable_features": [
            "Silicon Valley location",
            "Strong entrepreneurship programs",
            "Beautiful campus",
            "Diverse academic programs",
            "Research excellence"
        ],
        "website": "https://www.stanford.edu",
        "contact": {
            "phone": "(650) 723-2300",
            "email": "admission@stanford.edu"
        }
    },
    
    "berkeley": {
        "name": "University of California, Berkeley",
        "location": "Berkeley, California",
        "type": "Public Research University",
        "founded": 1868,
        "ranking": 4,
        "acceptance_rate": 14.5,
        "tuition": {
            "undergraduate_in_state": 14312,
            "undergraduate_out_state": 44007,
            "graduate": 29000,
            "room_board": 18000
        },
        "programs": {
            "undergraduate": [
                "Computer Science", "Engineering", "Business", "Biology", "Psychology",
                "Political Science", "Economics", "English", "History", "Mathematics",
                "Physics", "Chemistry", "Art", "Music", "Environmental Science"
            ],
            "graduate": [
                "Engineering", "Business", "Law", "Public Health", "Education",
                "Social Work", "Journalism", "Public Policy", "Architecture"
            ]
        },
        "admission_requirements": {
            "gpa": 3.7,
            "sat_score": 1430,
            "act_score": 32,
            "toefl": 80,
            "ielts": 7.0,
            "essays": 4,
            "recommendations": 0,
            "deadline": "November 30"
        },
        "campus_life": {
            "student_population": 45000,
            "undergraduate": 32000,
            "graduate": 13000,
            "international_students": 17,
            "student_faculty_ratio": 20,
            "housing": "Not guaranteed"
        },
        "notable_features": [
            "Top public university",
            "Diverse student body",
            "Strong research programs",
            "Liberal arts education",
            "Activist culture"
        ],
        "website": "https://www.berkeley.edu",
        "contact": {
            "phone": "(510) 642-6000",
            "email": "admissions@berkeley.edu"
        }
    },
    
    "yale": {
        "name": "Yale University",
        "location": "New Haven, Connecticut",
        "type": "Private Research University",
        "founded": 1701,
        "ranking": 5,
        "acceptance_rate": 6.2,
        "tuition": {
            "undergraduate": 59950,
            "graduate": 45000,
            "room_board": 18000
        },
        "programs": {
            "undergraduate": [
                "Liberal Arts", "Sciences", "Engineering", "Computer Science",
                "Economics", "Political Science", "Psychology", "Biology",
                "Chemistry", "Physics", "Mathematics", "English", "History"
            ],
            "graduate": [
                "Law", "Medicine", "Business", "Divinity", "Drama", "Music",
                "Art", "Architecture", "Forestry", "Public Health", "Nursing"
            ]
        },
        "admission_requirements": {
            "gpa": 3.9,
            "sat_score": 1515,
            "act_score": 34,
            "toefl": 100,
            "ielts": 7.0,
            "essays": 2,
            "recommendations": 2,
            "deadline": "January 2"
        },
        "campus_life": {
            "student_population": 15000,
            "undergraduate": 6000,
            "graduate": 9000,
            "international_students": 22,
            "student_faculty_ratio": 6,
            "housing": "Guaranteed for 4 years"
        },
        "notable_features": [
            "Ivy League member",
            "Residential college system",
            "World-class libraries",
            "Strong arts programs",
            "Global perspective"
        ],
        "website": "https://www.yale.edu",
        "contact": {
            "phone": "(203) 432-4771",
            "email": "admissions@yale.edu"
        }
    },
    
    "princeton": {
        "name": "Princeton University",
        "location": "Princeton, New Jersey",
        "type": "Private Research University",
        "founded": 1746,
        "ranking": 6,
        "acceptance_rate": 5.8,
        "tuition": {
            "undergraduate": 57190,
            "graduate": 57190,
            "room_board": 17000
        },
        "programs": {
            "undergraduate": [
                "Liberal Arts", "Engineering", "Computer Science", "Economics",
                "Politics", "Psychology", "Biology", "Chemistry", "Physics",
                "Mathematics", "English", "History", "Art", "Music"
            ],
            "graduate": [
                "Engineering", "Public Affairs", "Architecture", "Public Policy",
                "Finance", "Economics", "Mathematics", "Physics", "Chemistry"
            ]
        },
        "admission_requirements": {
            "gpa": 3.9,
            "sat_score": 1505,
            "act_score": 34,
            "toefl": 100,
            "ielts": 7.0,
            "essays": 2,
            "recommendations": 2,
            "deadline": "January 1"
        },
        "campus_life": {
            "student_population": 8500,
            "undergraduate": 5400,
            "graduate": 3100,
            "international_students": 25,
            "student_faculty_ratio": 5,
            "housing": "Guaranteed for 4 years"
        },
        "notable_features": [
            "Ivy League member",
            "No graduate business school",
            "Strong undergraduate focus",
            "Generous financial aid",
            "Beautiful campus"
        ],
        "website": "https://www.princeton.edu",
        "contact": {
            "phone": "(609) 258-3000",
            "email": "uaoffice@princeton.edu"
        }
    },
    
    "caltech": {
        "name": "California Institute of Technology",
        "location": "Pasadena, California",
        "type": "Private Research University",
        "founded": 1891,
        "ranking": 7,
        "acceptance_rate": 6.4,
        "tuition": {
            "undergraduate": 58680,
            "graduate": 58680,
            "room_board": 18000
        },
        "programs": {
            "undergraduate": [
                "Physics", "Chemistry", "Biology", "Mathematics", "Computer Science",
                "Engineering", "Geology", "Astronomy", "Economics", "English"
            ],
            "graduate": [
                "Physics", "Chemistry", "Biology", "Mathematics", "Computer Science",
                "Engineering", "Geology", "Astronomy", "Economics", "Social Science"
            ]
        },
        "admission_requirements": {
            "gpa": 3.9,
            "sat_score": 1545,
            "act_score": 35,
            "toefl": 90,
            "ielts": 7.0,
            "essays": 2,
            "recommendations": 2,
            "deadline": "January 3"
        },
        "campus_life": {
            "student_population": 2400,
            "undergraduate": 1000,
            "graduate": 1400,
            "international_students": 30,
            "student_faculty_ratio": 3,
            "housing": "Guaranteed for 4 years"
        },
        "notable_features": [
            "Small, focused institution",
            "World-class science programs",
            "Nobel Prize winners among faculty",
            "Strong research opportunities",
            "Collaborative environment"
        ],
        "website": "https://www.caltech.edu",
        "contact": {
            "phone": "(626) 395-6811",
            "email": "ugadmissions@caltech.edu"
        }
    },
    
    "columbia": {
        "name": "Columbia University",
        "location": "New York, New York",
        "type": "Private Research University",
        "founded": 1754,
        "ranking": 8,
        "acceptance_rate": 6.1,
        "tuition": {
            "undergraduate": 65000,
            "graduate": 65000,
            "room_board": 16000
        },
        "programs": {
            "undergraduate": [
                "Liberal Arts", "Engineering", "Business", "Journalism", "International Affairs",
                "Computer Science", "Economics", "Psychology", "Biology", "Chemistry",
                "Physics", "Mathematics", "English", "History", "Political Science"
            ],
            "graduate": [
                "Business", "Law", "Medicine", "Journalism", "International Affairs",
                "Engineering", "Arts and Sciences", "Public Health", "Social Work", "Education"
            ]
        },
        "admission_requirements": {
            "gpa": 3.9,
            "sat_score": 1510,
            "act_score": 34,
            "toefl": 100,
            "ielts": 7.0,
            "essays": 2,
            "recommendations": 2,
            "deadline": "January 1"
        },
        "campus_life": {
            "student_population": 33000,
            "undergraduate": 9000,
            "graduate": 24000,
            "international_students": 35,
            "student_faculty_ratio": 6,
            "housing": "Guaranteed for 4 years"
        },
        "notable_features": [
            "Ivy League member",
            "Located in New York City",
            "Strong journalism program",
            "Diverse student body",
            "Global perspective"
        ],
        "website": "https://www.columbia.edu",
        "contact": {
            "phone": "(212) 854-2522",
            "email": "ugrad-ask@columbia.edu"
        }
    },
    
    "upenn": {
        "name": "University of Pennsylvania",
        "location": "Philadelphia, Pennsylvania",
        "type": "Private Research University",
        "founded": 1740,
        "ranking": 9,
        "acceptance_rate": 8.4,
        "tuition": {
            "undergraduate": 61000,
            "graduate": 61000,
            "room_board": 17000
        },
        "programs": {
            "undergraduate": [
                "Business", "Engineering", "Liberal Arts", "Nursing", "Computer Science",
                "Economics", "Psychology", "Biology", "Chemistry", "Physics",
                "Mathematics", "English", "History", "Political Science", "International Relations"
            ],
            "graduate": [
                "Business", "Law", "Medicine", "Engineering", "Education",
                "Social Work", "Veterinary Medicine", "Dental Medicine", "Nursing"
            ]
        },
        "admission_requirements": {
            "gpa": 3.8,
            "sat_score": 1500,
            "act_score": 34,
            "toefl": 100,
            "ielts": 7.0,
            "essays": 2,
            "recommendations": 2,
            "deadline": "January 5"
        },
        "campus_life": {
            "student_population": 26000,
            "undergraduate": 10000,
            "graduate": 16000,
            "international_students": 20,
            "student_faculty_ratio": 6,
            "housing": "Guaranteed for 4 years"
        },
        "notable_features": [
            "Ivy League member",
            "Strong business school",
            "Interdisciplinary programs",
            "Urban campus",
            "Research opportunities"
        ],
        "website": "https://www.upenn.edu",
        "contact": {
            "phone": "(215) 898-7507",
            "email": "info@admissions.upenn.edu"
        }
    },
    
    "duke": {
        "name": "Duke University",
        "location": "Durham, North Carolina",
        "type": "Private Research University",
        "founded": 1838,
        "ranking": 10,
        "acceptance_rate": 8.6,
        "tuition": {
            "undergraduate": 60000,
            "graduate": 60000,
            "room_board": 16000
        },
        "programs": {
            "undergraduate": [
                "Liberal Arts", "Engineering", "Business", "Public Policy", "Computer Science",
                "Economics", "Psychology", "Biology", "Chemistry", "Physics",
                "Mathematics", "English", "History", "Political Science", "Environmental Science"
            ],
            "graduate": [
                "Business", "Law", "Medicine", "Engineering", "Public Policy",
                "Divinity", "Nursing", "Environment", "Education"
            ]
        },
        "admission_requirements": {
            "gpa": 3.8,
            "sat_score": 1490,
            "act_score": 34,
            "toefl": 100,
            "ielts": 7.0,
            "essays": 2,
            "recommendations": 2,
            "deadline": "January 2"
        },
        "campus_life": {
            "student_population": 16000,
            "undergraduate": 7000,
            "graduate": 9000,
            "international_students": 15,
            "student_faculty_ratio": 6,
            "housing": "Guaranteed for 4 years"
        },
        "notable_features": [
            "Strong athletics program",
            "Beautiful campus",
            "Research excellence",
            "Global programs",
            "Interdisciplinary approach"
        ],
        "website": "https://www.duke.edu",
        "contact": {
            "phone": "(919) 684-3214",
            "email": "askduke@duke.edu"
        }
    },
    
    "northwestern": {
        "name": "Northwestern University",
        "location": "Evanston, Illinois",
        "type": "Private Research University",
        "founded": 1851,
        "ranking": 11,
        "acceptance_rate": 9.3,
        "tuition": {
            "undergraduate": 60000,
            "graduate": 60000,
            "room_board": 16000
        },
        "programs": {
            "undergraduate": [
                "Liberal Arts", "Engineering", "Journalism", "Communication", "Computer Science",
                "Economics", "Psychology", "Biology", "Chemistry", "Physics",
                "Mathematics", "English", "History", "Political Science", "Theater"
            ],
            "graduate": [
                "Business", "Law", "Medicine", "Engineering", "Journalism",
                "Communication", "Education", "Music", "Social Work"
            ]
        },
        "admission_requirements": {
            "gpa": 3.8,
            "sat_score": 1490,
            "act_score": 34,
            "toefl": 100,
            "ielts": 7.0,
            "essays": 2,
            "recommendations": 2,
            "deadline": "January 2"
        },
        "campus_life": {
            "student_population": 22000,
            "undergraduate": 8000,
            "graduate": 14000,
            "international_students": 18,
            "student_faculty_ratio": 6,
            "housing": "Guaranteed for 4 years"
        },
        "notable_features": [
            "Strong journalism program",
            "Lakefront campus",
            "Research opportunities",
            "Diverse programs",
            "Chicago proximity"
        ],
        "website": "https://www.northwestern.edu",
        "contact": {
            "phone": "(847) 491-7271",
            "email": "ug-admission@northwestern.edu"
        }
    },
    
    "jhu": {
        "name": "Johns Hopkins University",
        "location": "Baltimore, Maryland",
        "type": "Private Research University",
        "founded": 1876,
        "ranking": 12,
        "acceptance_rate": 11.2,
        "tuition": {
            "undergraduate": 58000,
            "graduate": 58000,
            "room_board": 15000
        },
        "programs": {
            "undergraduate": [
                "Liberal Arts", "Engineering", "Public Health", "International Studies", "Computer Science",
                "Economics", "Psychology", "Biology", "Chemistry", "Physics",
                "Mathematics", "English", "History", "Political Science", "Neuroscience"
            ],
            "graduate": [
                "Medicine", "Public Health", "Engineering", "Business", "Education",
                "International Studies", "Nursing", "Arts and Sciences"
            ]
        },
        "admission_requirements": {
            "gpa": 3.8,
            "sat_score": 1480,
            "act_score": 33,
            "toefl": 100,
            "ielts": 7.0,
            "essays": 2,
            "recommendations": 2,
            "deadline": "January 2"
        },
        "campus_life": {
            "student_population": 32000,
            "undergraduate": 6000,
            "graduate": 26000,
            "international_students": 22,
            "student_faculty_ratio": 7,
            "housing": "Guaranteed for 4 years"
        },
        "notable_features": [
            "World-renowned medical school",
            "Strong research programs",
            "Public health leadership",
            "International focus",
            "Baltimore location"
        ],
        "website": "https://www.jhu.edu",
        "contact": {
            "phone": "(410) 516-8171",
            "email": "gotojhu@jhu.edu"
        }
    },
    
    "cornell": {
        "name": "Cornell University",
        "location": "Ithaca, New York",
        "type": "Private Research University",
        "founded": 1865,
        "ranking": 13,
        "acceptance_rate": 10.6,
        "tuition": {
            "undergraduate": 61000,
            "graduate": 61000,
            "room_board": 15000
        },
        "programs": {
            "undergraduate": [
                "Liberal Arts", "Engineering", "Agriculture", "Business", "Computer Science",
                "Economics", "Psychology", "Biology", "Chemistry", "Physics",
                "Mathematics", "English", "History", "Political Science", "Hotel Administration"
            ],
            "graduate": [
                "Business", "Law", "Medicine", "Engineering", "Agriculture",
                "Veterinary Medicine", "Hotel Administration", "Industrial Relations"
            ]
        },
        "admission_requirements": {
            "gpa": 3.8,
            "sat_score": 1480,
            "act_score": 33,
            "toefl": 100,
            "ielts": 7.0,
            "essays": 2,
            "recommendations": 2,
            "deadline": "January 2"
        },
        "campus_life": {
            "student_population": 24000,
            "undergraduate": 15000,
            "graduate": 9000,
            "international_students": 25,
            "student_faculty_ratio": 9,
            "housing": "Guaranteed for 4 years"
        },
        "notable_features": [
            "Ivy League member",
            "Beautiful campus",
            "Diverse programs",
            "Strong agriculture school",
            "Research excellence"
        ],
        "website": "https://www.cornell.edu",
        "contact": {
            "phone": "(607) 255-5241",
            "email": "admissions@cornell.edu"
        }
    },
    
    "rice": {
        "name": "Rice University",
        "location": "Houston, Texas",
        "type": "Private Research University",
        "founded": 1912,
        "ranking": 14,
        "acceptance_rate": 11.1,
        "tuition": {
            "undergraduate": 52000,
            "graduate": 52000,
            "room_board": 15000
        },
        "programs": {
            "undergraduate": [
                "Liberal Arts", "Engineering", "Business", "Architecture", "Computer Science",
                "Economics", "Psychology", "Biology", "Chemistry", "Physics",
                "Mathematics", "English", "History", "Political Science", "Music"
            ],
            "graduate": [
                "Business", "Engineering", "Architecture", "Music", "Education",
                "Public Policy", "Social Sciences", "Natural Sciences"
            ]
        },
        "admission_requirements": {
            "gpa": 3.8,
            "sat_score": 1480,
            "act_score": 33,
            "toefl": 100,
            "ielts": 7.0,
            "essays": 2,
            "recommendations": 2,
            "deadline": "January 1"
        },
        "campus_life": {
            "student_population": 8000,
            "undergraduate": 4000,
            "graduate": 4000,
            "international_students": 20,
            "student_faculty_ratio": 6,
            "housing": "Guaranteed for 4 years"
        },
        "notable_features": [
            "Small, intimate environment",
            "Strong engineering programs",
            "Houston location",
            "Research opportunities",
            "Diverse student body"
        ],
        "website": "https://www.rice.edu",
        "contact": {
            "phone": "(713) 348-7423",
            "email": "admission@rice.edu"
        }
    },
    
    "vanderbilt": {
        "name": "Vanderbilt University",
        "location": "Nashville, Tennessee",
        "type": "Private Research University",
        "founded": 1873,
        "ranking": 15,
        "acceptance_rate": 12.3,
        "tuition": {
            "undergraduate": 56000,
            "graduate": 56000,
            "room_board": 15000
        },
        "programs": {
            "undergraduate": [
                "Liberal Arts", "Engineering", "Business", "Education", "Computer Science",
                "Economics", "Psychology", "Biology", "Chemistry", "Physics",
                "Mathematics", "English", "History", "Political Science", "Music"
            ],
            "graduate": [
                "Business", "Law", "Medicine", "Engineering", "Education",
                "Nursing", "Divinity", "Graduate School"
            ]
        },
        "admission_requirements": {
            "gpa": 3.8,
            "sat_score": 1470,
            "act_score": 33,
            "toefl": 100,
            "ielts": 7.0,
            "essays": 2,
            "recommendations": 2,
            "deadline": "January 1"
        },
        "campus_life": {
            "student_population": 13000,
            "undergraduate": 7000,
            "graduate": 6000,
            "international_students": 12,
            "student_faculty_ratio": 7,
            "housing": "Guaranteed for 4 years"
        },
        "notable_features": [
            "Beautiful campus",
            "Strong music program",
            "Nashville location",
            "Research opportunities",
            "Diverse programs"
        ],
        "website": "https://www.vanderbilt.edu",
        "contact": {
            "phone": "(615) 322-2561",
            "email": "admissions@vanderbilt.edu"
        }
    }
}

def get_college_by_name(college_name: str) -> Optional[Dict]:
    """Get college information by name (case-insensitive)"""
    college_name = college_name.lower().replace(" ", "").replace("university", "").replace("college", "")
    
    # Direct name mapping
    name_mapping = {
        "harvard": "harvard",
        "mit": "mit",
        "stanford": "stanford",
        "berkeley": "berkeley",
        "yale": "yale",
        "princeton": "princeton",
        "caltech": "caltech",
        "columbia": "columbia",
        "upenn": "upenn",
        "penn": "upenn",
        "duke": "duke",
        "northwestern": "northwestern",
        "jhu": "jhu",
        "johnshopkins": "jhu",
        "johns": "jhu",
        "cornell": "cornell",
        "rice": "rice",
        "vanderbilt": "vanderbilt",
        "ucberkeley": "berkeley",
        "uc": "berkeley",
        "massachusetts": "mit",
        "california": "stanford",
        "pennsylvania": "upenn",
        "texas": "rice",
        "tennessee": "vanderbilt",
        "illinois": "northwestern",
        "maryland": "jhu",
        "newyork": "columbia",
        "northcarolina": "duke"
    }
    
    college_key = name_mapping.get(college_name)
    if college_key and college_key in COLLEGES_DATA:
        return COLLEGES_DATA[college_key]
    
    # Search by partial name
    for key, college in COLLEGES_DATA.items():
        if college_name in college["name"].lower():
            return college
    
    return None

def get_all_colleges() -> List[Dict]:
    """Get list of all colleges"""
    return list(COLLEGES_DATA.values())

def search_colleges_by_program(program: str) -> List[Dict]:
    """Search colleges by program of study"""
    matching_colleges = []
    program_lower = program.lower()
    
    for college in COLLEGES_DATA.values():
        # Check undergraduate programs
        for ug_program in college["programs"]["undergraduate"]:
            if program_lower in ug_program.lower():
                matching_colleges.append(college)
                break
        
        # Check graduate programs if not found in undergraduate
        if college not in matching_colleges:
            for grad_program in college["programs"]["graduate"]:
                if program_lower in grad_program.lower():
                    matching_colleges.append(college)
                    break
    
    return matching_colleges

def search_colleges_by_location(location: str) -> List[Dict]:
    """Search colleges by location"""
    matching_colleges = []
    location_lower = location.lower()
    
    for college in COLLEGES_DATA.values():
        if location_lower in college["location"].lower():
            matching_colleges.append(college)
    
    return matching_colleges

def compare_colleges(college_names: List[str]) -> Dict:
    """Compare multiple colleges"""
    colleges = []
    for name in college_names:
        college = get_college_by_name(name)
        if college:
            colleges.append(college)
    
    if len(colleges) < 2:
        return {"error": "Need at least 2 colleges to compare"}
    
    comparison = {
        "colleges": colleges,
        "comparison": {
            "tuition": {college["name"]: college["tuition"] for college in colleges},
            "acceptance_rate": {college["name"]: college["acceptance_rate"] for college in colleges},
            "ranking": {college["name"]: college["ranking"] for college in colleges},
            "student_population": {college["name"]: college["campus_life"]["student_population"] for college in colleges}
        }
    }
    
    return comparison

def get_admission_calculator(college_name: str, gpa: float, sat: int, act: int = None) -> Dict:
    """Calculate admission chances based on stats"""
    college = get_college_by_name(college_name)
    if not college:
        return {"error": "College not found"}
    
    requirements = college["admission_requirements"]
    acceptance_rate = college["acceptance_rate"]
    
    # Simple scoring system
    score = 0
    max_score = 100
    
    # GPA scoring (40% weight)
    gpa_score = min((gpa / requirements["gpa"]) * 40, 40)
    score += gpa_score
    
    # SAT scoring (30% weight)
    if sat:
        sat_score = min((sat / requirements["sat_score"]) * 30, 30)
        score += sat_score
    
    # ACT scoring (30% weight)
    if act:
        act_score = min((act / requirements["act_score"]) * 30, 30)
        score += act_score
    
    # Determine admission chance
    if score >= 90:
        chance = "Very High"
        color = "green"
    elif score >= 80:
        chance = "High"
        color = "lightgreen"
    elif score >= 70:
        chance = "Moderate"
        color = "yellow"
    elif score >= 60:
        chance = "Low"
        color = "orange"
    else:
        chance = "Very Low"
        color = "red"
    
    return {
        "college": college["name"],
        "score": round(score, 1),
        "chance": chance,
        "color": color,
        "acceptance_rate": acceptance_rate,
        "requirements": requirements
    }
