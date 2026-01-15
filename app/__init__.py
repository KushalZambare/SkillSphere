from flask import Flask
import os


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
    
    # Register blueprints
    from app.blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.blueprints.recommendation import bp as recommendation_bp
    app.register_blueprint(recommendation_bp)
    
    from app.blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    return app
