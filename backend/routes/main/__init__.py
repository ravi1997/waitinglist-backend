from flask import Blueprint

bp = Blueprint('main', __name__)

from backend.routes.main import routes