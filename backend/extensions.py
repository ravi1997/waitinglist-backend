import click
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt 

# Create db object. This db object will be imported in various model definitions
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()
bcrypt = Bcrypt() 

def print_rows(x):
    for row in x:
        print(row)


# Import various models that have inherited the db object and have defined the tables, field, relationships etc