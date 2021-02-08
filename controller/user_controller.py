from flask import Blueprint, redirect, flash, render_template, session, request, url_for, current_app
from flask_principal import identity_changed, Identity, AnonymousIdentity
from controller.helpers.authorize import verify_role, auth_required_with_role, get_home_route
from repository.user_repository import UserRepository
from service.user_service import UserService

auth = Blueprint('auth', __name__)

userRepo = UserRepository()
userService = UserService(userRepo)

@auth.route("/")
def home():
    return render_template("home.html")


@auth.route('/login', methods=["POST", "GET"])
def login():
    if id in session and session["id"]:
        return redirect(url_for(get_home_route()))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]


        
        try:
            found_user = userService.getOneByUsername(username)
        except ValueError as err:
            flash("Incorect credentials!")
            return render_template("user/login.html")

        session.permanent = True
        session["username"] = username
        session["id"] = userService.getOneByUsername(username).get_id()

        if found_user and found_user.get_password() == password:
            if (found_user.get_role() == 0):
                session["role"] = 0
                return redirect(url_for("student.home"))
            if (found_user.get_role() == 1):
                session["role"] = 1
                return redirect(url_for("responsabil_firma.home"))
            if (found_user.get_role() == 2):
                session["role"] = 2
                return redirect(url_for("tutore_firma.home"))
            if (found_user.get_role() == 3):
                session["role"] = 3
                return redirect(url_for("secretara.home"))
            if (found_user.get_role() == 4):
                session["role"] = 4
                return redirect(url_for("protectia_muncii.home"))
            if (found_user.get_role() == 5):
                session["role"] = 5
                return redirect(url_for("cadru_didactic_supervizor.home"))
            if (found_user.get_role() == 6):
                session["role"] = 6
                return redirect(url_for("responsabil_facultate.home"))
            if (found_user.get_role() == 7):
                session["role"] = 7
                return redirect(url_for("decan.home"))
            else:
                return render_template("user/login.html")
        else:
            flash("Incorect password!")
            return render_template("user/login.html")
    else:  # GET
        if "user" in session:
            flash("Already logged in!")
            return render_template("user/login.html")
        return render_template("user/login.html")


@auth.route("/logout")
def logout():
    if "username" in session:
        flash("You have been logged out!", "info")

    session.pop("username", None)
    session.pop("role", None)
    session.pop("id", None)
    return redirect(url_for("auth.login"))
