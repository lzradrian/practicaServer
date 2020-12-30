from flask import Blueprint, render_template, session, request, url_for

from controller.helpers.authorize import verify_role

responsabil_facultate = Blueprint('responsabil_facultate', __name__)


@responsabil_facultate.route('/responsabil_facultate', methods=["GET"])
def home():
    if verify_role(6) == 0:
        return render_template("home.html")
    return render_template("responsabilFacultate/homeResponsabilFacultate.html")
