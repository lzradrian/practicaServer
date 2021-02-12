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
    return redirect(url_for("auth.login"))

@auth.route("/admin", methods=["POST", "GET"])
def admin():
    from controller import db
    

    if request.method == "POST":
        user_id = request.form["user_id"]
        accepted = request.form["accepted"]

        if accepted == "0": #nu-acceptat
            try:
                user = userService.getOne(user_id)  
                db.session.delete(user)
                db.session.commit()
            except:
                pass
            
        else:  #acceptat
            user = userService.getOne(user_id) 
            user.is_accepted = 1
            db.session.commit()
            pass
    
    accounts = userService.getAll()
    pending_accounts = list() 
    for a in accounts: 
        if a.is_accepted == False: 
            pending_accounts.append(a)

    return render_template("user/admin.html", pending_accounts=pending_accounts)
        

@auth.route("/register", methods=["POST", "GET"])
def register(): 
    if request.method == "POST":
        #POST METHOD
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        account_type = request.form["account_type"]

        if password != confirm_password :
            flash("The two password don't match!")
            return render_template("user/register.html")
        try:
            if userService.getOneByUsername(username):
                flash("There is already one account with this username!")
                return render_template("user/register.html")
        except:
            from domain.user import User 
            from controller import db
            user = User(username, password, "", account_type)
            db.session.add(user)
            db.session.commit()
            flash("Account registered successfully!")
            return redirect(url_for("auth.login"))
    else:
        #GET Method:
        return render_template("user/register.html")


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
        if(found_user.is_accepted == 0):
            flash("Your account is still pending admin's approval!")
            return render_template("user/login.html")

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
            if(found_user.get_role() == 100): # admin
                session["role"] = 100 
                return redirect(url_for("auth.admin"))

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
