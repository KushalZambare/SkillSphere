from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class UserProfile:
    name: str
    age: int
    current_grade: str
    academic_subjects: List[str]
    grades: Dict[str, str]
    interests: List[str]
    hobbies: List[str]
    preferred_work_environment: str
    career_goals: Optional[str] = None
    location_preference: str = "Any"
    budget_range: str = "Medium"

@dataclass
class CareerRecommendation:
    career_title: str
    description: str
    required_skills: List[str]
    education_path: str
    job_prospects: str
    salary_range: str
    growth_potential: str

@dataclass
class CollegeRecommendation:
    college_name: str
    location: str
    programs: List[str]
    ranking: str
    admission_requirements: str
    fees_range: str
    notable_features: str
