from flask import Blueprint, redirect, flash, render_template, session, request, url_for

from controller.helpers.authorize import verify_role, get_home_route

protectia_muncii = Blueprint('protectia_muncii', __name__)


@protectia_muncii.route('/protectia_muncii', methods=["GET"])
def home():
    if verify_role(4) == 0:
        return  redirect(url_for(get_home_route()))
    return render_template("protectiaMuncii/homeProtectiaMuncii.html")
