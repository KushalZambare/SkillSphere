from flask import request, jsonify
from core.models import UserProfile, CareerRecommendation, CollegeRecommendation
from core.utils import make_ai_request, parse_career_response, parse_college_response  # Fixed the typo
from typing import List

class CareerRecommendationSystem:
    """AI-powered Career Recommendation System using Google AI REST API"""
    
    def __init__(self, api_key: str):
        """Initialize the system with Google AI API key"""
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    
    def generate_career_recommendations(self, user_profile: UserProfile) -> List[CareerRecommendation]:
        """Generate career recommendations using Google AI"""
        
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
        
        response_text = make_ai_request(self.api_key, self.base_url, prompt)
        if response_text:
            return parse_career_response(response_text)
        return []
    
    def generate_college_recommendations(self, user_profile: UserProfile, career_recommendations: List[CareerRecommendation]) -> List[CollegeRecommendation]:
        """Generate college recommendations based on user profile and career choices"""
        
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
        
        response_text = make_ai_request(self.api_key, self.base_url, prompt)
        if response_text:
            return parse_college_response(response_text)
        return []
    
    def generate_roadmap(self, user_profile: UserProfile, career_recommendations: List[CareerRecommendation]) -> str:
        """Generate a detailed roadmap for the user"""
        
        prompt = f"""
        Create a detailed 5-year roadmap for {user_profile.name} based on their profile and career recommendations:

        Student Profile:
        - Current Grade: {user_profile.current_grade}
        - Age: {user_profile.age}
        - Academic Strengths: {', '.join([f"{subject}({grade})" for subject, grade in user_profile.grades.items()])}
        - Interests: {', '.join(user_profile.interests)}

        Top Career Options: {', '.join([career.career_title for career in career_recommendations[:3]])}

        Create a roadmap with these sections:
        
        IMMEDIATE STEPS (Next 6 months):
        - [Specific actions to take now]
        
        SHORT-TERM GOALS (6 months - 2 years):
        - [Academic and skill development goals]
        
        MEDIUM-TERM GOALS (2-4 years):
        - [College and advanced preparation]
        
        LONG-TERM VISION (4-5 years):
        - [Career entry and growth]

        For each phase, include specific, actionable items related to:
        - Academic focus areas
        - Skill development priorities
        - Extracurricular activities
        - Networking opportunities
        - Certification/course recommendations
        - Milestone achievements

        Make it practical and tailored to their current situation.
        """
        
        response_text = make_ai_request(self.api_key, self.base_url, prompt)
        return response_text if response_text else "Unable to generate roadmap at this time."
    
    def display_career_recommendations(self, careers: List[CareerRecommendation]):
        """Display career recommendations in a formatted way"""
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
        """Display college recommendations in a formatted way"""
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