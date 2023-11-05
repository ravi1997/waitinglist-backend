from flask import Blueprint

bp = Blueprint('cadre', __name__)

from backend.routes.cadre import routes