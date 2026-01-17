from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

# Initialize extensions (will be initialized in create_app)
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app(config_class=None):
    """
    Application factory pattern for Flask.
    Creates and configures the Flask application instance.
    """
    app = Flask(__name__, 
                static_folder='../static', 
                static_url_path='/static',
                template_folder='../templates')
    
    # Configuration
    if config_class:
        app.config.from_object(config_class)
    else:
        # Default configuration
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
        app.config['API_KEY'] = os.environ.get('API_KEY', 'Your API Key')
        # Database configuration
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # User loader callback
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
    # Import models to ensure they are registered with SQLAlchemy
    from app.models import User, Roadmap
    
    # Register blueprints
    from app.blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.blueprints.recommendation import bp as recommendation_bp
    app.register_blueprint(recommendation_bp)
    
    from app.blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    return app
