from flask import Blueprint , redirect,flash,render_template,session,request,url_for

users = Blueprint('users',__name__)
auth = Blueprint('auth', __name__)

from repository.user_repository import UserRepository
from service.user_service import UserService

userRepo = UserRepository()
userService = UserService(userRepo)


@users.route('/')
def index():
    #return "hello"
    return render_template("home.html")



@auth.route('/login',methods=["POST","GET"])
def login():
    if request.method=="POST":
        session.permanent = True
        username= request.form["username"]
        password = request.form["password"]
        session["user"]=username

        try:
            found_user = userService.getOneByUsername(username)
        except ValueError as err:
            flash("Incorect credentials!")
            return render_template("login.html")

        if found_user and found_user.get_password() == password:
            flash("Login succesful!")
            return redirect(url_for("users.user"))


    else:
        if "user" in session:
            flash("Already logged in!")
            return redirect(url_for("users.user"))
        return render_template("login.html")


@users.route("/user",methods=["POST","GET"])
def user():
    email=None

    if request.method == "POST":
         email=request.form["email"]

    email=None
    if "user" in session:
        user=session["user"]
        if request.method=="POST":
            email=request.form["email"]
            session["email"]=email
            flash("email was saved")
        else:
            if "email" in session:
                email=session["email"]
        return render_template("user.html",email=email)
    else:
        flash("You are not logged in!")
        return redirect(url_for("auth.login"))

#din AcordPractica.html (ce contine un form) obtinem datele: nume firma, adresa etc
#cazuri posibile: cu aceste date sa generam un nou acord.html completat (si apoi transformat in pdf)
#libraria: Dominate
@users.route("/user/acordPractica", methods=["POST", "GET"])
def userAcordPractica():
    if request.method == "POST":
        numeFirma = request.form["numeFirma"]
        print("numeFirma obtinut din form: ",numeFirma)

        return render_template("home.html")
    else:
        return render_template("AcordPractica.html")

@users.route("/logout")
def logout():
    if "user" in session:
        user=session["user"]
        flash("You have been logged out!", "info")
    session.pop("user",None)
    session.pop("email", None)

    return redirect(url_for("auth.login"))
