from flask import Blueprint

bp = Blueprint('recommendation', __name__)

from app.blueprints.recommendation import routes
