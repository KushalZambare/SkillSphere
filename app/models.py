from dataclasses import dataclass
from typing import Dict, List, Optional
from app import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

# SQLAlchemy Database Models

class User(UserMixin, db.Model):
    """
    User model for authentication and user management.
    Inherits from UserMixin for Flask-Login compatibility.
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    
    # Relationship: One user can have multiple roadmaps
    roadmaps = db.relationship('Roadmap', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set the password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Roadmap(db.Model):
    """
    Roadmap model to store user career roadmaps.
    """
    __tablename__ = 'roadmaps'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)  
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    
    def __repr__(self):
        return f'<Roadmap {self.id} for User {self.user_id}>'

# Dataclasses for application logic (kept for backward compatibility)

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
