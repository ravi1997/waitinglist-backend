from flask import Blueprint

bp = Blueprint('account', __name__)

from backend.routes.account import routes