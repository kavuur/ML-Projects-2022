from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import SQLAlchemyError, OperationalError

login_manager = LoginManager()
db = SQLAlchemy()
bcrypt = Bcrypt()