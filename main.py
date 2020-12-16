from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app=Flask(__name__)

#app.config.from_object('database.database_config.Config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite3'

db = SQLAlchemy(app)


from controller import user_controller
app.register_blueprint(user_controller.auth)
app.register_blueprint(user_controller.users)

#db.create_all()

app.run()



#if __name__ == '__main__':
#    from service.user_service import UserService
#    from repository.user_repository import UserRepository


#    # baza de date nu creeaza automat tabelul pentru modelul User


#    #repo = UserRepository()
#    #service = UserService(repo)
#    #user1 = User( 1,"username1", "pas1","email","role")
#    #service.add(user1)



