from flask import render_template, request, current_app
from app.blueprints.recommendation import bp
from core.user_input import create_user_profile
from core.recommendation_system import CareerRecommendationSystem
from core.utils import save_recommendations


@bp.route('/submit', methods=['POST'])
def submit():
    """
    Handles form submission and generates career/college recommendations.
    """
    # Get API key from app config
    api_key = current_app.config.get('API_KEY', 'Your API Key')
    system = CareerRecommendationSystem(api_key)
    
    # Create user profile from form data
    user_profile = create_user_profile(request.form)
    
    # Generate recommendations
    career_recommendations = system.generate_career_recommendations(user_profile)
    college_recommendations = system.generate_college_recommendations(user_profile, career_recommendations)
    roadmap = system.generate_roadmap(user_profile, career_recommendations)
    
    # Save recommendations if requested
    if request.form.get('save'):
        save_recommendations(user_profile, career_recommendations, college_recommendations, roadmap)
    
    return render_template('results.html', 
                         user_profile=user_profile, 
                         career_recommendations=career_recommendations, 
                         college_recommendations=college_recommendations, 
                         roadmap=roadmap)
