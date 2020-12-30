from flask import Blueprint , redirect,flash,render_template,session,request,url_for

from controller.helpers.authorize import verify_role

secretara = Blueprint('secretara',__name__)


@secretara.route('/secretara',methods=["POST","GET"])
def home():
    if request.method == "POST":
        if request.form.get('secretaraAcordButton'):
            pass
        elif request.form.get("secretaraProtectieButton"):
            pass
        elif request.form.get("secretaraConventieButton"):
            pass


    else:
        if verify_role(3) == 0:
            return render_template("home.html")
        return render_template("homeSecretara.html")