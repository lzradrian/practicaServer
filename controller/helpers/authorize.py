from functools import wraps, update_wrapper

import flask
from flask import url_for, request, redirect, session, render_template, g
# from flask_principal import Permission, RoleNeed

from repository.user_repository import UserRepository
from service.user_service import UserService

userRepo = UserRepository()
userService = UserService(userRepo)

def get_home_route():
    if "role" not in session:
        print("role not in session. redirecting to login")
        return None

    if session["role"] == 0:
        return "student.home"
    elif session["role"] == 1:
        return "responsabil_firma.home"
    elif session["role"] == 2:
        return "tutore_firma.home"
    elif session["role"] == 3:
        return "secretara.home"
    elif session["role"] == 5: 
        return "cadru_didactic_supervizor.home"
    elif session["role"] == 6:
        return "responsabil_facultate.home"
    elif session["role"] == 7:
        return "decan.home"
def verify_role(role):
    '''
    :param role: int
    :return: 1 if current user role is equal to given param
             0 otherwise
    '''

    if "role" not in session:
        print("role not in session")
        return 0
    elif session["role"] != role:
        print("role not =role")
        return 0
    return 1


# tried to create a decorator function to check for authentification and role
# not working
def auth_required_with_role(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):

            if "role" not in session:
                return redirect(url_for('auth.login'))
            elif session["role"] != role:
                print("role not =role")
                return redirect(url_for('auth.login'))

            return f(*args, **kwargs)

        return decorated_function

    return decorator
