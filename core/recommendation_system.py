from flask import request, jsonify
from app.models import UserProfile, CareerRecommendation, CollegeRecommendation
from core.utils import make_ai_request, parse_career_response, parse_college_response
from typing import List

class CareerRecommendationSystem:
    
    def __init__(self, api_key: str, model: str = "google/gemini-2.0-flash-001"):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = model
    
    def generate_career_recommendations(self, user_profile: UserProfile) -> List[CareerRecommendation]:
        
        prompt = f"""
        Based on the following student profile, provide 5 personalized career recommendations:

        Student Profile:
        - Name: {user_profile.name}
        - Age: {user_profile.age}
        - Current Grade: {user_profile.current_grade}
        - Academic Subjects: {', '.join(user_profile.academic_subjects)}
        - Grades: {', '.join([f"{subject}: {grade}" for subject, grade in user_profile.grades.items()])}
        - Interests: {', '.join(user_profile.interests)}
        - Hobbies: {', '.join(user_profile.hobbies)}
        - Preferred Work Environment: {user_profile.preferred_work_environment}
        - Career Goals: {user_profile.career_goals or 'Not specified'}
        - Location Preference: {user_profile.location_preference}

        For each career recommendation, provide the information in this EXACT format:

        CAREER 1:
        Career Title: [Title]
        Description: [2-3 sentence description]
        Required Skills: [skill1, skill2, skill3, skill4, skill5]
        Education Path: [specific degrees and certifications needed]
        Job Prospects: [current market demand]
        Salary Range: [approximate figures]
        Growth Potential: [future outlook]

        CAREER 2:
        [Same format]

        Continue for 5 careers total.
        """
        
        response_text = make_ai_request(self.api_key, self.base_url, prompt, self.model)
        if response_text:
            return parse_career_response(response_text)
        return []
    
    def generate_college_recommendations(self, user_profile: UserProfile, career_recommendations: List[CareerRecommendation]) -> List[CollegeRecommendation]:
        
        career_titles = [career.career_title for career in career_recommendations[:3]]
        
        prompt = f"""
        Based on the student profile and career interests, recommend 8 colleges/universities:

        Student Profile:
        - Current Grade: {user_profile.current_grade}
        - Academic Subjects: {', '.join(user_profile.academic_subjects)}
        - Grades: {', '.join([f"{subject}: {grade}" for subject, grade in user_profile.grades.items()])}
        - Location Preference: {user_profile.location_preference}
        - Budget Range: {user_profile.budget_range}
        
        Career Interests: {', '.join(career_titles)}

        For each college recommendation, provide the information in this EXACT format:

        COLLEGE 1:
        College Name: [Name]
        Location: [City, Country]
        Programs: [program1, program2, program3]
        Ranking: [approximate ranking or tier]
        Admission Requirements: [key requirements]
        Fees Range: [approximate annual fees]
        Notable Features: [2-3 key highlights]

        COLLEGE 2:
        [Same format]

        Continue for 8 colleges total. Focus on institutions that are accessible based on current academic performance and aligned with location/budget preferences.
        """
        
        response_text = make_ai_request(self.api_key, self.base_url, prompt, self.model)
        if response_text:
            return parse_college_response(response_text)
        return []
    
    def generate_roadmap(self, user_profile: UserProfile, career_recommendations: List[CareerRecommendation]) -> List[dict]:
        
        prompt = f"""
        Create a detailed 5-year roadmap for {user_profile.name} based on their profile and career recommendations.
        Return the response as a valid JSON object ONLY, with no preamble or markdown formatting.
        
        The JSON structure should be a list of phases:
        [
          {{
            "title": "Phase Title (e.g. IMMEDIATE STEPS)",
            "period": "Time period (e.g. Next 6 months)",
            "objective": "Brief objective for this phase",
            "action_items": [
              {{
                "category": "Academic/Skill/Extracurricular/etc",
                "task": "Specific actionable task"
              }}
            ],
            "milestones": ["Milestone 1", "Milestone 2"]
          }}
        ]

        Student Profile:
        - Current Grade: {user_profile.current_grade}
        - Age: {user_profile.age}
        - Academic Strengths: {', '.join([f"{subject}({grade})" for subject, grade in user_profile.grades.items()])}
        - Interests: {', '.join(user_profile.interests)}

        Top Career Options: {', '.join([career.career_title for career in career_recommendations[:3]])}

        Create 4 phases:
        1. IMMEDIATE STEPS (Next 6 months)
        2. SHORT-TERM GOALS (6 months - 2 years)
        3. MEDIUM-TERM GOALS (2-4 years)
        4. LONG-TERM VISION (4-5 years)

        For each phase, include specific, actionable items related to:
        - Academic focus areas
        - Skill development priorities
        - Extracurricular activities
        - Networking opportunities
        - Certification/course recommendations
        """
        
        response_text = make_ai_request(self.api_key, self.base_url, prompt, self.model)
        
        if response_text:
            try:
                clean_json = response_text.strip()
                if clean_json.startswith("```json"):
                    clean_json = clean_json[7:-3].strip()
                elif clean_json.startswith("```"):
                    clean_json = clean_json[3:-3].strip()
                
                import json
                return json.loads(clean_json)
            except Exception as e:
                print(f"Error parsing roadmap JSON: {e}")
                print(f"Raw response: {response_text[:200]}...")
        
        return []
    
    def display_career_recommendations(self, careers: List[CareerRecommendation]):
        print("\n" + "="*60)
        print("CAREER RECOMMENDATIONS")
        print("="*60)
        
        for i, career in enumerate(careers, 1):
            print(f"\n{i}. {career.career_title}")
            print("-" * (len(career.career_title) + 3))
            print(f"Description: {career.description}")
            print(f"Required Skills: {', '.join(career.required_skills)}")
            print(f"Education Path: {career.education_path}")
            print(f"Job Prospects: {career.job_prospects}")
            print(f"Salary Range: {career.salary_range}")
            print(f"Growth Potential: {career.growth_potential}")
            print()
    
    def display_college_recommendations(self, colleges: List[CollegeRecommendation]):
        print("\n" + "="*60)
        print("COLLEGE RECOMMENDATIONS")
        print("="*60)
        
        for i, college in enumerate(colleges, 1):
            print(f"\n{i}. {college.college_name}")
            print("-" * (len(college.college_name) + 3))
            print(f"Location: {college.location}")
            print(f"Relevant Programs: {', '.join(college.programs)}")
            print(f"Ranking: {college.ranking}")
            print(f"Admission Requirements: {college.admission_requirements}")
            print(f"Fees Range: {college.fees_range}")
            print(f"Notable Features: {college.notable_features}")
            print()
    
    def display_roadmap(self, roadmap: str):
        """Display the generated roadmap"""
        print("\n" + "="*60)
        print("PERSONALIZED ROADMAP")
        print("="*60)
        print(roadmap)
