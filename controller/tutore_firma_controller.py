from flask import Blueprint , redirect,flash,render_template,session,request,url_for

tutore_firma = Blueprint('tutore_firma',__name__)


@tutore_firma.route('/tutore_firma',methods=["POST","GET"])
def home():
    if request.method == "POST":
        if request.form.get('tutoreFirmaConventieButton'):
            #return render_template("tutoreFirmaConventieButton.html")
            print("ok")
            pass

    else:
        return render_template("homeTutoreFirma.html")