from database.database_config import Config

def run():
    from main import db
    db.create_all()
    print("database created!")


run()
