from flask import Blueprint, redirect, flash, render_template, session, request, url_for

from controller.helpers.authorize import verify_role

secretara = Blueprint('secretara', __name__)


@secretara.route('/secretara', methods=["GET"])
def home():
    if verify_role(3) == 0:
        return render_template("home.html")
    return render_template("secretara/homeSecretara.html")
