from flask import Blueprint , redirect,flash,render_template,session,request,url_for

student = Blueprint('student',__name__)


@student.route('/student',methods=["POST","GET"])
def home():
    if request.method == "POST":
        if request.form.get('studentFirmaButton'):
            pass
            #return render_template("studentbutton1.html")
        elif request.form.get("studentUbbButton"):
            pass
        elif request.form.get("studentTraseuButton"):
            pass
        elif request.form.get("documentButton"):
            pass

    else:
        return render_template("homeStudent.html")



