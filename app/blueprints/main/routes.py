from flask import render_template
from app.blueprints.main import bp


@bp.route('/')
def index():
    """Landing page - displays the user profile form."""
    return render_template('index.html')
