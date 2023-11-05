from flask import Blueprint

bp = Blueprint('auth', __name__)

from backend.routes.auth import routes