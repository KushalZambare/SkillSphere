from flask import Flask, render_template, request, redirect, url_for, flash
from core.user_input import create_user_profile
from core.recommendation_system import CareerRecommendationSystem
from core.utils import save_recommendations
import requests  

app = Flask(__name__)
app.secret_key = "dev-secret-key"


# Use Your API Key
API_KEY = "Your API Key"
system = CareerRecommendationSystem(API_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        user_profile = create_user_profile(request.form)
    except ValueError as e:
        flash(str(e), "error")
        return redirect(url_for('index'))

    career_recommendations = system.generate_career_recommendations(user_profile)
    college_recommendations = system.generate_college_recommendations(
        user_profile, career_recommendations
    )
    roadmap = system.generate_roadmap(user_profile, career_recommendations)

    if request.form.get('save'):
        save_recommendations(user_profile, career_recommendations, college_recommendations, roadmap)

    return render_template(
        'results.html',
        user_profile=user_profile,
        career_recommendations=career_recommendations,
        college_recommendations=college_recommendations,
        roadmap=roadmap
    )

if __name__ == '__main__':
    app.run(debug=True)
