from backend.routes.main import bp


@bp.route('/')
def index():
    return 'This is The waiting list application'