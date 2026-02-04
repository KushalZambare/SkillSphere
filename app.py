from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager
from core.utils import parse_resume, save_recommendations
from core.user_input import create_user_profile
from core.recommendation_system import CareerRecommendationSystem
import os

app = Flask(__name__, 
            static_folder='static', 
            template_folder='templates')

app.secret_key = 'super_secret_key_change_this_in_production'

# === 1. CONNECT DATABASE (CRITICAL FIX) ===
# We must configure the DB and connect it to the app, 
# otherwise 'User.query' crashes in the auth routes.

# A. Configure the Database URI (Using standard SQLite path)
# If your DB is named differently (e.g., database.db), update the name below.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# B. Import and Initialize 'db'
# We try to find where your 'db' object is defined (usually app/__init__.py or app/extensions.py)
try:
    from app import db
    db.init_app(app)
except ImportError:
    try:
        from app.extensions import db
        db.init_app(app)
    except ImportError:
        print("WARNING: Could not find 'db' object to initialize. Login might fail.")

# === 2. SETUP FLASK-LOGIN ===
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login' 

@login_manager.user_loader
def load_user(user_id):
    # We need to import the User model to load the user
    try:
        from app.models import User
        return User.query.get(int(user_id))
    except ImportError:
        return None

# === 3. REGISTER BLUEPRINTS ===

# Auth Blueprint
try:
    from app.blueprints.auth.routes import auth as auth_bp
    app.register_blueprint(auth_bp)
except (ImportError, AttributeError):
    try:
        from app.blueprints.auth.routes import bp as auth_bp
        app.register_blueprint(auth_bp)
    except Exception as e:
        print(f"Auth Blueprint Warning: {e}")

# Recommendation Blueprint
try:
    from app.blueprints.recommendation.routes import recommendation as rec_bp
    app.register_blueprint(rec_bp)
except (ImportError, AttributeError):
    try:
        from app.blueprints.recommendation.routes import bp as rec_bp
        app.register_blueprint(rec_bp)
    except Exception as e:
        print(f"Recommendation Blueprint Warning: {e}")

# Main Blueprint
try:
    from app.blueprints.main.routes import main as main_bp
    app.register_blueprint(main_bp)
except (ImportError, AttributeError):
    try:
        from app.blueprints.main.routes import bp as main_bp
        app.register_blueprint(main_bp)
    except Exception as e:
        pass # If main blueprint fails, we have the fallback route below

# === 4. ROUTES ===

API_KEY = "You API Key"
system = CareerRecommendationSystem(API_KEY)

# Homepage (Ensures no 404)
@app.route('/')
def index():
    return render_template('index.html')

# Resume Parser (New Feature)
@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['resume']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file:
        try:
            data = parse_resume(file, file.filename)
            if data is None:
                return jsonify({'error': 'Unsupported file type'}), 400
            
            return jsonify(data)
        except Exception as e:
            print(f"Resume Parsing Error: {e}")
            return jsonify({'error': str(e)}), 500
            
    return jsonify({'error': 'Unknown error'}), 500

# Submit Form
@app.route('/submit', methods=['POST'])
def submit():
    try:
        user_profile = create_user_profile(request.form)
    except ValueError as e:
        return render_template("index.html", error=str(e))

    career_recommendations = system.generate_career_recommendations(user_profile)
    college_recommendations = system.generate_college_recommendations(
        user_profile, career_recommendations
    )
    roadmap = system.generate_roadmap(user_profile, career_recommendations)

    if request.form.get('save'):
        save_recommendations(
            user_profile,
            career_recommendations,
            college_recommendations,
            roadmap
        )

    return render_template(
        'results.html',
        user_profile=user_profile,
        career_recommendations=career_recommendations,
        college_recommendations=college_recommendations,
        roadmap=roadmap
    )

if __name__ == '__main__':
    app.run(debug=True)