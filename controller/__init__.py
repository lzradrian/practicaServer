from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from controller import user_controller
from controller import student_controller
from controller import tutore_firma_controller
from controller import responsabil_facultate_controller
from controller import secretara_controller
from controller import responsabil_firma_controller
from controller import cadru_didactic_supervizor_controller
from controller import decan_controller

app = Flask(__name__)
app.register_blueprint(user_controller.auth)
app.register_blueprint(student_controller.student)
app.register_blueprint(tutore_firma_controller.tutore_firma)
app.register_blueprint(responsabil_facultate_controller.responsabil_facultate)
app.register_blueprint(secretara_controller.secretara)
app.register_blueprint(responsabil_firma_controller.responsabil_firma)
app.register_blueprint(cadru_didactic_supervizor_controller.cadru_didactic_supervizor)
app.register_blueprint(decan_controller.decan)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = '123abc7891337'
app.config.from_object('database.database_config.Config')
db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run()
