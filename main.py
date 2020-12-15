from flask import Flask, render_template
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from controller import user_controller


#app.secret_key="secret_key"

#app.permanent_session_lifetime=timedelta(minutes=10) #store pemanent data session for x time


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False

app.register_blueprint(user_controller.auth)
app.register_blueprint(user_controller.users)

#cors = CORS(app) #posibil sa ne ajute flask-Cors
#app.config['CORS_HEADERS'] = 'Content-Type'

app.config['SECRET_KEY'] = '123'
#app.config.from_object('database.database_config.Config')
db = SQLAlchemy(app)





if __name__ == '__main__':
    from service.user_service import UserService
    from repository.user_repository import UserRepository
    from domain.user import User

    #repo = UserRepository()
    #service = UserService(repo)
    #user1 = User( 1,"username1", "pas1")
    #service.add(user1)

    # baza de date nu creeaza automat tabelul pentru modelul User
    db.create_all()

    app.run(debug=True)

