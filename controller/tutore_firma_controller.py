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
            line = "AcknowledgementTutorName " + name + "\n"
        if "AcknowledgementSupervisorFunction" in line:
            line = "AcknowledgementSupervisorFunction " + function + "\n"

        # todo: replace signature (did not find in conventie_input.txt)
        replaced_content = replaced_content + line
    print(conventie.get_content())
    conventie.set_content(replaced_content)
    conventie.set_completedByFirmaTutori(True)

    conventieRepo = ConventieRepository()
    conventieService = ConventieService(conventieRepo)
    conventieService.update(conventie)


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
