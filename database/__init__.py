#from database.database_config import Config

from domain.user import User


def run():
    from main import db
    db.create_all()
    print("database created!")


run()
