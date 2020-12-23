from flask import Blueprint , redirect,flash,render_template,session,request,url_for

from repository.user_repository import UserRepository
from service.user_service import UserService

auth = Blueprint('auth', __name__)

userRepo = UserRepository()
userService = UserService(userRepo)


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
            if (found_user.get_role()==0):
                return redirect(url_for("student.home"))
            if (found_user.get_role()==1):
                pass
            if (found_user.get_role()==2):
                return redirect(url_for("tutore_firma.home"))
            if (found_user.get_role()==3):
                return redirect(url_for("secretara.home"))
            if (found_user.get_role()==4):
                pass
            if (found_user.get_role()==5):
                pass
            if (found_user.get_role()==6):
                return redirect(url_for("responsabil_facultate.home"))
            if (found_user.get_role()==7):
                pass
            else:
                return render_template("login.html")
        else:
            #print("wrong pass")
            flash("Incorect credentials!")
            return render_template("login.html")
    else: #GET
        if "user" in session:
            flash("Already logged in!")
            return redirect(url_for("users.user"))
        return render_template("login.html")


@auth.route("/logout")
def logout():
    if "user" in session:
        user=session["user"]
        flash("You have been logged out!", "info")
    session.pop("user",None)
    session.pop("email", None)

    return redirect(url_for("auth.login"))
