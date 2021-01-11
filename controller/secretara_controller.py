from flask import Blueprint, redirect, flash, render_template, session, request, url_for

from controller.helpers.authorize import verify_role, get_home_route

secretara = Blueprint('secretara', __name__)


@secretara.route('/secretara', methods=["GET"])
def home():
    if verify_role(3) == 0:
        return  redirect(url_for(get_home_route()))
    return render_template("secretara/homeSecretara.html")
