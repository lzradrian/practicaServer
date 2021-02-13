from flask import Blueprint, redirect, flash, render_template, session, request, url_for

from controller.helpers.authorize import verify_role, get_home_route
from repository.conventie_repository import ConventieRepository
from service.conventie_service import ConventieService
from repository.student_internship_repository import StudentInternshipRepository
from service.student_internship_serivce import StudentInternshipService
from repository.student_info_repository import StudentInfoRepository
from service.student_info_service import StudentInfoService
from repository.tutor_info_repository import TutorInfoRepository
from service.tutor_info_service import TutorInfoService

tutore_firma = Blueprint('tutore_firma', __name__)


def modify_conventie_input(conventie, name, function, signature):
    '''
    Actualizeaza contentul conventiei din baza de date cu datele primite ca parametrii
    '''
    content = conventie.get_content()
    replaced_content = ""

    from io import StringIO
    s = StringIO(content)
    for line in s:
        if "AcknowledgementTutorName" in line:
            line = "AcknowledgementTutorName " + name
        if "AcknowledgementSupervisorFunction" in line:
            line = "AcknowledgementSupervisorFunction " + function
        if "TutorSignature" in line:
            line = "TutorSignature "+ signature
        replaced_content = replaced_content + line +"\n"
    print(conventie.get_content())
    conventie.set_content(replaced_content)
    conventie.set_completedByFirmaTutori(True)

    conventieRepo = ConventieRepository()
    conventieService = ConventieService(conventieRepo)
    conventieService.update(conventie)



@tutore_firma.route('/evaluare', methods=["POST", "GET"])
def evaluare(): 
    if request.method == "POST":
        from openpyxl import load_workbook
        import os 

        workbook = load_workbook(filename=os.getcwd() + '/evaluare.xlsx')
        sheet = workbook.active
        
        sheet["A6"] = request.form["companyname"]
        sheet["E7"] = request.form["companynumber"]
        sheet["G7"] = request.form["companycity"]

        sheet["D12"] = request.form["studentname"]
        sheet["B14"] = request.form["studentschool"]
        sheet["B16"] = request.form["studentspecialty"]
        sheet["B18"] = request.form["studentyear"]

        sheet["D20"] = request.form["tutorname"]
        sheet["B22"] = request.form["companyname"]
        sheet["B23"] = request.form["companyphone"]
        sheet["B24"] = request.form["companymail"]

        sheet["D26"] = request.form["startdate"]
        sheet["D28"] = request.form["enddate"]
        sheet["D31"] = request.form["hoursdone"]
        try:
            if(request.form["companydomain1"] == "on"):
                sheet["D37"] = "X"
            if(request.form["companydomain2"] == "on"):
                sheet["D38"] = "X"
            if(request.form["companydomain3"] == "on"):
                sheet["D39"] = "X"
            if(request.form["companydomain4"] == "on"):
                sheet["D40"] = request.form["otherdomain"]
        except:
            pass

        try:
            if(request.form["studentactivity1"] == "on"):
                sheet["F45"] = "X"
            if(request.form["studentactivity2"] == "on"):
                sheet["F46"] = "X"
            if(request.form["studentactivity3"] == "on"):
                sheet["F47"] = "X"
            if(request.form["studentactivity4"] == "on"):
                sheet["F48"] = "X"
            if(request.form["studentactivity5"] == "on"):
                sheet["F49"] = request.form["otheractivity"]
        except:
            pass

        try:
            if request.form["startgrade"] == "0": 
                sheet["A59"] = "X"
            if request.form["startgrade"] == "1":
                sheet["B59"] = "X"
            if request.form["startgrade"] == "2":
                sheet["C59"] = "X"
            if request.form["startgrade"] == "3":
                sheet["D59"] = "X"
            if request.form["startgrade"] == "4":
                sheet["E59"] = "X"

        except BaseException as ex: 
            pass

        try:
            if request.form["workgrade"] == "0": 
                sheet["A65"] = "X"
            if request.form["workgrade"] == "1":
                sheet["B65"] = "X"
            if request.form["workgrade"] == "2":
                sheet["C65"] = "X"
            if request.form["workgrade"] == "3":
                sheet["D65"] = "X"
            if request.form["workgrade"] == "4":
                sheet["E65"] = "X"

        except BaseException as ex: 
            pass

        try:
            if request.form["docgrade"] == "0": 
                sheet["A71"] = "X"
            if request.form["docgrade"] == "1":
                sheet["B71"] = "X"
            if request.form["docgrade"] == "2":
                sheet["C71"] = "X"
            if request.form["docgrade"] == "3":
                sheet["D71"] = "X"
            if request.form["docgrade"] == "4":
                sheet["D71"] = "X"

        except BaseException as ex: 
            pass

        sheet["D77"] = request.form["algorithmgrade"]
        sheet["D78"] = request.form["programminggrade"]
        sheet["D79"] = request.form["architecturegrade"]
        sheet["D80"] = request.form["methodgrade"]
        sheet["D81"] = request.form["databasegrade"]
        
        sheet["D82"] = request.form["osgrade"]
        sheet["D83"] = request.form["testgrade"]    
        sheet["D84"] = request.form["securitygrade"]
        sheet["B85"] = request.form["otherspecialty"]
        sheet["D85"] = request.form["othergrade"]

        try:
            if request.form["taskgrade"] == "0": 
                sheet["A100"] = "X"
            if request.form["taskgrade"] == "1":
                sheet["B100"] = "X"
            if request.form["taskgrade"] == "2":
                sheet["C100"] = "X"
            if request.form["taskgrade"] == "3":
                sheet["D100"] = "X"

        except BaseException as ex: 
            pass

        try:
            if request.form["taskgrade"] == "0": 
                sheet["A106"] = "X"
            if request.form["taskgrade"] == "1":
                sheet["B106"] = "X"
            if request.form["taskgrade"] == "2":
                sheet["C106"] = "X"
            if request.form["taskgrade"] == "3":
                sheet["D106"] = "X"

        except BaseException as ex: 
            pass

        try:
            if request.form["studentactivity1"] == "on": 
                sheet["D111"] = "0.5"
            if request.form["studentactivity2"] == "on":
                sheet["D112"] = "0.5"
            if request.form["studentactivity3"] == "on":
                sheet["D113"] = "0.5"
            if request.form["studentactivity4"] == "on":
                sheet["D114"] = "0.5"
            if request.form["studentactivity5"] == "on":
                sheet["D115"] = "0.5"
            if request.form["studentactivity6"] == "on":
                sheet["D116"] = "0.5"

        except BaseException as ex: 
            pass

        sheet["A125"] = request.form["date"]

        workbook.save(filename=os.getcwd() + '/evaluare_result.xlsx')
        from flask import send_file
        return send_file(os.getcwd() + '/evaluare_result.xlsx', as_attachment=True)

    return render_template("firmaTutore/evaluare.html")

@tutore_firma.route('/conventie_tutore_firma', methods=["POST", "GET"])
def conventie():
    tInfoRepo = TutorInfoRepository()
    tInfoServ = TutorInfoService(tInfoRepo)
    conventiiDeModificat = []
    conventieRepo = ConventieRepository()
    conventieService = ConventieService(conventieRepo)
    studentInternshipRepo = StudentInternshipRepository()
    studentInternshipServ = StudentInternshipService(studentInternshipRepo)
    conventii = conventieService.getAll()
    for conventie in conventii:
        try:
            if studentInternshipServ.getOne(conventie.get_id()).tutor_id == session["id"]:
                if conventie.get_completedByStudent() == True and conventie.get_completedByFirmaTutori() == False:
                    conventiiDeModificat.append(conventie)
                    print("s-a adaugat conventia cu id-ul:", conventie.get_id())
        except:
            continue

    if request.method == "POST":
        # tutorname = request.form["tutorname"]
        # tutorfunction = request.form["tutorfunction"]
        info = tInfoServ.getOne(session["id"])
        tutorname = info.name
        tutorfunction = info.function
        signature = request.form["signature"]

        repoStudInf = StudentInfoRepository()
        servStudInf = StudentInfoService(repoStudInf)
        numeStudenti = []
        for conventie in conventiiDeModificat:
            modify_conventie_input(conventie, tutorname, tutorfunction, signature)
            numeStudenti.append(servStudInf.getOne(conventie.get_id()).name)
        mesaj = "Ati modificat cu succes conventiile urmatorilor studenti: "
        for nume in numeStudenti:
            mesaj = mesaj + str(nume) + "; "
        flash(mesaj)

        return render_template("firmaTutore/homeTutoreFirma.html")
    else:  # GET
        try:
            info = tInfoServ.getOne(session["id"])

            if len(conventiiDeModificat) == 0:
                flash("Nu sunt conventii de completat!")
                return render_template("firmaTutore/homeTutoreFirma.html")
            return render_template("firmaTutore/conventieTutoreFirma.html")
        except:
            flash("Completati datele generale inainte de completarea conventiei!")
            # return render_template("student/homeStudent.html")
            return render_template("firmaTutore/homeTutoreFirma.html")


@tutore_firma.route('/info', methods=["POST", "GET"])
def info():
    if request.method == "POST":
        from service.utility import get_tutor_info_service
        from domain.tutor_info import TutorInfo

        service = get_tutor_info_service()
        id = session["id"]
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        fax = request.form["fax"]
        function = request.form["function"]

        try:
            service.add(TutorInfo(id, name, email, phone, fax, function))
            flash("Ati completat cu succes datele!")
        except:
            service.update(TutorInfo(id, name, email, phone, fax, function))
            flash("Ati updatat cu succes datele!")

        return render_template("firmaTutore/homeTutoreFirma.html")
    return render_template("firmaTutore/infoTutoreFirma.html")


@tutore_firma.route('/tutore_firma', methods=["GET"])
def home():
    if verify_role(2) == 0:
        return redirect(url_for(get_home_route()))
    return render_template("firmaTutore/homeTutoreFirma.html")
