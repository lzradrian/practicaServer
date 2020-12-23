from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from controller import user_controller

from controller import student_controller
from controller import tutore_firma_controller
from controller import responsabil_facultate_controller
from controller import secretara_controller

app = Flask(__name__)
app.register_blueprint(user_controller.auth)
app.register_blueprint(student_controller.student)
app.register_blueprint(tutore_firma_controller.tutore_firma)
app.register_blueprint(responsabil_facultate_controller.responsabil_facultate)
app.register_blueprint(secretara_controller.secretara)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = '123abc7891337'
app.config.from_object('database.database_config.Config')
db = SQLAlchemy(app)



if __name__ == '__main__':

    #from repository.user_repository import UserRepository
    #from service.user_service import UserService
    #userRepo = UserRepository()
    #userService = UserService(userRepo)
    #from domain.user import User
    #user1 = User(1,"admin","admin","email","role")
    #userService.add(user1)

    app.run()

