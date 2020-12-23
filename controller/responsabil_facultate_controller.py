from flask import Blueprint , render_template,session,request,url_for

responsabil_facultate = Blueprint('responsabil_facultate',__name__)


@responsabil_facultate.route('/responsabil_facultate',methods=["POST","GET"])
def home():
    if request.method == "POST":
        if request.form.get('responsabilFacultateAcordButton'):
            pass
            #return render_template("--.html")

    else:
        return render_template("homeResponsabilFacultate.html")