from database.database_config import Config
from flask_sqlalchemy import SQLAlchemy
from domain.user import User


def run():
    from controller import db
    db.create_all()


run()
