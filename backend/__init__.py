# python package
import click
from flask import Flask


def create_app():
	app = Flask(__name__, instance_relative_config=False)
	from config import ProdConfig, DevConfig
	app.config.from_object(ProdConfig)
	
	# Import the Initialized Flask extensions  
	# Import the db object and various models that have inherited the db object
	from .extensions import db, migrate, ma, jwt, bcrypt
	
	with app.app_context():
		# Set global values
		# Initialize globals
		db.init_app(app)
		migrate.init_app(app, db)
		ma.init_app(app)
		jwt.init_app(app)
		bcrypt.init_app(app)

		# Import Models
		# Used by Flask-Migrate
		import backend.models_import

		# Register the " flask --app backend init-db" command
		from backend.db_initializer.db_initializer import seed_db_command, empty_db_command
		app.cli.add_command(seed_db_command)
		app.cli.add_command(empty_db_command)


		# Registering routes
		from backend.routes import main_bp,auth_bp,patient_bp,department_bp,cadre_bp
	
		app.register_blueprint(main_bp,url_prefix='/waitinglist')
		app.register_blueprint(auth_bp,url_prefix='/waitinglist/auth')
		app.register_blueprint(patient_bp,url_prefix='/waitinglist/patient')    
		app.register_blueprint(department_bp,url_prefix='/waitinglist/department')    
		app.register_blueprint(cadre_bp,url_prefix='/waitinglist/cadre')    
	return app

