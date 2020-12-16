from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from controller import user_controller

app = Flask(__name__)
app.register_blueprint(user_controller.auth)
app.register_blueprint(user_controller.users)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = '123abc7891337'
app.config.from_object('database.database_config.Config')
db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run()

