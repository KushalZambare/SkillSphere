import requests
import json
from typing import List, Dict
from app.models import CareerRecommendation, CollegeRecommendation, UserProfile

def make_ai_request(api_key: str, url: str, prompt: str) -> str:
  
    try:
        headers = {
            "Content-Type": "application/json",
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        
        params = {
            "key": api_key
        }
        
        response = requests.post(url, headers=headers, json=data, params=params, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        if "candidates" in result and len(result["candidates"]) > 0:
            return result["candidates"][0]["content"]["parts"][0]["text"]
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
    
    careers = []
    try:
        sections = response_text.split('CAREER ')
        
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
                    key, value = line.split(':', 1)
                    key = key.strip().lower().replace(' ', '_')
                    value = value.strip()
                    
                    if key == 'career_title':
                        career_data['career_title'] = value
                    elif key == 'description':
                        career_data['description'] = value
                    elif key == 'required_skills':
                        career_data['required_skills'] = [s.strip() for s in value.split(',')]
                    elif key == 'education_path':
                        career_data['education_path'] = value
                    elif key == 'job_prospects':
                        career_data['job_prospects'] = value
                    elif key == 'salary_range':
                        career_data['salary_range'] = value
                    elif key == 'growth_potential':
                        career_data['growth_potential'] = value
                    current_field = key
                elif current_field and current_field not in ['required_skills']:
                    career_data[current_field] += ' ' + line
            
            if career_data['career_title'] and career_data['description']:
                careers.append(CareerRecommendation(**career_data))
                
            if len(careers) >= 5:
                break
    
    except Exception as e:
        print(f"Error parsing career response: {e}")
    
    return careers

def parse_college_response(response_text: str) -> List[CollegeRecommendation]:
    
    colleges = []
    try:
        sections = response_text.split('COLLEGE ')
        
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
                    key, value = line.split(':', 1)
                    key = key.strip().lower().replace(' ', '_')
                    value = value.strip()
                    
                    if key == 'college_name':
                        college_data['college_name'] = value
                    elif key == 'location':
                        college_data['location'] = value
                    elif key == 'programs':
                        college_data['programs'] = [s.strip() for s in value.split(',')]
                    elif key == 'ranking':
                        college_data['ranking'] = value
                    elif key == 'admission_requirements':
                        college_data['admission_requirements'] = value
                    elif key == 'fees_range':
                        college_data['fees_range'] = value
                    elif key == 'notable_features':
                        college_data['notable_features'] = value
                    current_field = key
                elif current_field and current_field not in ['programs']:
                    college_data[current_field] += ' ' + line
            
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
            f.write(roadmap)
        
        print(f"\nRecommendations saved to: {filename}")
        
    except Exception as e:

        print(f"Error saving recommendations: {e}")
