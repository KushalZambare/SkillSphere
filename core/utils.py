import requests
import json
from typing import List, Dict
from app.models import CareerRecommendation, CollegeRecommendation, UserProfile

def make_ai_request(api_key: str, url: str, prompt: str, model: str = "google/gemini-2.0-flash-001") -> str:
  
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://github.com/KushalZambare/SkillSphere", 
            "X-Title": "SkillSphere Career Guidance", 
        }
        
        data = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        
        # DEBUG LOGGING
        with open("raw_api_response.log", "a", encoding="utf-8") as f:
            f.write("=== NEW REQUEST ===\n")
            f.write(json.dumps(result, indent=2))
            f.write("\n\n")
            
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        else:
            print(f"Unexpected API response format: {result}")
            return ""
        
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response status: {e.response.status_code}")
            try:
                error_data = e.response.json()
                print(f"Error details: {error_data}")
            except:
                print(f"Response text: {e.response.text[:200]}...")
        return ""
    except requests.exceptions.Timeout:
        print("Request timed out. Please check your internet connection.")
        return ""
    except requests.exceptions.ConnectionError:
        print("Connection error. Please check your internet connection.")
        return ""
    except Exception as e:
        print(f"Error making AI request: {e}")
        return ""

def parse_career_response(response_text: str) -> List[CareerRecommendation]:
    import re
    careers = []
    try:
        # Case-insensitive split on CAREER [digit]:
        sections = re.split(r'(?i)CAREER\s*\d*[:\s-]*', response_text)
        
        for section in sections[1:]:
            lines = section.strip().split('\n')
            career_data = {
                "career_title": "",
                "description": "",
                "required_skills": [],
                "education_path": "",
                "job_prospects": "",
                "salary_range": "",
                "growth_potential": ""
            }
            
            current_field = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                if ':' in line:
                    key_raw, value = line.split(':', 1)
                    key = re.sub(r'[^a-z0-9\s]', '', key_raw.lower()).strip().replace(' ', '_')
                    value = value.strip()
                    
                    if 'career_title' in key:
                        career_data['career_title'] = value
                    elif 'description' in key:
                        career_data['description'] = value
                    elif 'required_skills' in key or 'skills' in key:
                        career_data['required_skills'] = [s.strip() for s in value.split(',')]
                    elif 'education_path' in key:
                        career_data['education_path'] = value
                    elif 'job_prospects' in key:
                        career_data['job_prospects'] = value
                    elif 'salary_range' in key:
                        career_data['salary_range'] = value
                    elif 'growth_potential' in key:
                        career_data['growth_potential'] = value
                    current_field = key
                elif current_field:
                    lookup_field = None
                    if 'career_title' in current_field: lookup_field = 'career_title'
                    elif 'description' in current_field: lookup_field = 'description'
                    elif 'education_path' in current_field: lookup_field = 'education_path'
                    elif 'job_prospects' in current_field: lookup_field = 'job_prospects'
                    elif 'salary_range' in current_field: lookup_field = 'salary_range'
                    elif 'growth_potential' in current_field: lookup_field = 'growth_potential'
                    
                    if lookup_field and lookup_field != 'required_skills':
                        career_data[lookup_field] += ' ' + line
            
            if career_data['career_title'] and career_data['description']:
                careers.append(CareerRecommendation(**career_data))
                
            if len(careers) >= 5:
                break
    
    except Exception as e:
        print(f"Error parsing career response: {e}")
    
    return careers

def parse_college_response(response_text: str) -> List[CollegeRecommendation]:
    import re
    colleges = []
    try:
        sections = re.split(r'(?i)COLLEGE\s*\d*[:\s-]*', response_text)
        
        for section in sections[1:]:
            lines = section.strip().split('\n')
            college_data = {
                "college_name": "",
                "location": "",
                "programs": [],
                "ranking": "",
                "admission_requirements": "",
                "fees_range": "",
                "notable_features": ""
            }
            
            current_field = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                if ':' in line:
                    key_raw, value = line.split(':', 1)
                    key = re.sub(r'[^a-z0-9\s]', '', key_raw.lower()).strip().replace(' ', '_')
                    value = value.strip()
                    
                    if 'college_name' in key:
                        college_data['college_name'] = value
                    elif 'location' in key:
                        college_data['location'] = value
                    elif 'programs' in key:
                        college_data['programs'] = [s.strip() for s in value.split(',')]
                    elif 'ranking' in key:
                        college_data['ranking'] = value
                    elif 'admission_requirements' in key:
                        college_data['admission_requirements'] = value
                    elif 'fees_range' in key:
                        college_data['fees_range'] = value
                    elif 'notable_features' in key:
                        college_data['notable_features'] = value
                    current_field = key
                elif current_field:
                    lookup_field = None
                    if 'college_name' in current_field: lookup_field = 'college_name'
                    elif 'location' in current_field: lookup_field = 'location'
                    elif 'ranking' in current_field: lookup_field = 'ranking'
                    elif 'admission_requirements' in current_field: lookup_field = 'admission_requirements'
                    elif 'fees_range' in current_field: lookup_field = 'fees_range'
                    elif 'notable_features' in current_field: lookup_field = 'notable_features'
                    
                    if lookup_field and lookup_field != 'programs':
                        college_data[lookup_field] += ' ' + line
            
            if college_data['college_name'] and college_data['location']:
                colleges.append(CollegeRecommendation(**college_data))
                
            if len(colleges) >= 8:
                break
    
    except Exception as e:
        print(f"Error parsing college response: {e}")
    
    return colleges

def save_recommendations(user_profile: UserProfile, career_recommendations: List[CareerRecommendation], 
                        college_recommendations: List[CollegeRecommendation], roadmap: str):

    try:
        filename = f"{user_profile.name.replace(' ', '_')}_recommendations.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write("=== GYANSETU CAREER GUIDANCE REPORT ===\n\n")
            f.write(f"Student: {user_profile.name}\n")
            f.write(f"Age: {user_profile.age}\n")
            f.write(f"Current Grade: {user_profile.current_grade}\n\n")
            
            f.write("=== CAREER RECOMMENDATIONS ===\n")
            for i, career in enumerate(career_recommendations, 1):
                f.write(f"\n{i}. {career.career_title}\n")
                f.write(f"Description: {career.description}\n")
                f.write(f"Required Skills: {', '.join(career.required_skills)}\n")
                f.write(f"Education Path: {career.education_path}\n")
                f.write(f"Job Prospects: {career.job_prospects}\n")
                f.write(f"Salary Range: {career.salary_range}\n")
                f.write(f"Growth Potential: {career.growth_potential}\n\n")
            
            f.write("\n=== COLLEGE RECOMMENDATIONS ===\n")
            for i, college in enumerate(college_recommendations, 1):
                f.write(f"\n{i}. {college.college_name}\n")
                f.write(f"Location: {college.location}\n")
                f.write(f"Programs: {', '.join(college.programs)}\n")
                f.write(f"Ranking: {college.ranking}\n")
                f.write(f"Admission Requirements: {college.admission_requirements}\n")
                f.write(f"Fees Range: {college.fees_range}\n")
                f.write(f"Notable Features: {college.notable_features}\n\n")
            
            f.write("\n=== PERSONALIZED ROADMAP ===\n")
            if isinstance(roadmap, list):
                for phase in roadmap:
                    f.write(f"\n{phase.get('title', 'Phase')} ({phase.get('period', 'TBD')})\n")
                    f.write(f"Objective: {phase.get('objective', '')}\n")
                    f.write("Actions:\n")
                    for item in phase.get('action_items', []):
                        f.write(f"  - [{item.get('category', '')}] {item.get('task', '')}\n")
                    if phase.get('milestones'):
                        f.write("Milestones: " + ", ".join(phase['milestones']) + "\n")
            else:
                f.write(roadmap)
        
        print(f"\nRecommendations saved to: {filename}")
        
    except Exception as e:

        print(f"Error saving recommendations: {e}")
