from flask import Blueprint, render_template, session, request, url_for, redirect

from controller.helpers.authorize import verify_role, get_home_route

responsabil_facultate = Blueprint('responsabil_facultate', __name__)


@responsabil_facultate.route('/responsabil_facultate', methods=["GET"])
def home():
    if verify_role(6) == 0:
        return  redirect(url_for(get_home_route()))
    return render_template("responsabilFacultate/homeResponsabilFacultate.html")
