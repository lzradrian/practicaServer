from flask import Blueprint, redirect, flash, render_template, session, request, url_for

from controller.helpers.authorize import verify_role, get_home_route
from repository.conventie_repository import ConventieRepository
from service.conventie_service import ConventieService
from repository.student_internship_repository import StudentInternshipRepository
from service.student_internship_serivce import StudentInternshipService
from repository.supervisor_info_repository import SupervisorInfoRepository
from service.supervisor_info_service import SupervisorInfoService
from repository.student_info_repository import StudentInfoRepository
from service.student_info_service import StudentInfoService
cadru_didactic_supervizor = Blueprint('cadru_didactic_supervizor', __name__)


def modify_conventie_input(conventie, nume,functie,email,phone,fax):
    '''
    Actualizeaza contentul conventiei din baza de date cu datele primite ca parametrii
    '''
    content = conventie.get_content()
    replaced_content = ""

    from io import StringIO
    s = StringIO(content)
    for line in s:
        line = line.replace("SupervisorFunction Function", "SupervisorFunction " + nume)
        line = line.replace("SupervisorName Name", "SupervisorName " + functie)
        line = line.replace("SupervisorEmail Email", "SupervisorEmail " + email)
        line = line.replace("SupervisorPhone Phone", "SupervisorPhone " + phone)
        line = line.replace("SupervisorFax Fax", "SupervisorFax " + fax)
        # todo: alte date

        replaced_content = replaced_content + line

    conventie.set_content(replaced_content)
    conventie.set_completedByCadruDidacticSupervizor(True)

    conventieRepo = ConventieRepository()
    conventieService = ConventieService(conventieRepo)
    conventieService.update(conventie)


@cadru_didactic_supervizor.route('/conventie_cadru_didactic_supervizor', methods=["POST", "GET"])
def conventie():
    supervizorRepo = SupervisorInfoRepository()
    supervizorService = SupervisorInfoService(supervizorRepo)
    conventiiDeModificat = []
    conventieRepo = ConventieRepository()
    conventieService = ConventieService(conventieRepo)
    studentInternshipRepo = StudentInternshipRepository()
    studentInternshipServ = StudentInternshipService(studentInternshipRepo)
    conventii = conventieService.getAll()
    for conventie in conventii:
        try:
            if studentInternshipServ.getOne(conventie.get_id()).supervisor_id == session["id"]:
                if conventie.get_completedByStudent() == True and conventie.get_completedByFirmaResponsabil() == True and conventie.get_completedByFirmaTutori() == True and conventie.get_completedByCadruDidacticSupervizor() == False:
                    conventiiDeModificat.append(conventie)
        except:
            continue

    if request.method == "POST":
        info = supervizorService.getOne(session["id"])
        nume = info.name
        functie= info.specialization
        email=info.email
        phone=info.phone
        fax=info.fax
        signature = request.form["signature"] #todo


        repoStudInf = StudentInfoRepository()
        servStudInf = StudentInfoService(repoStudInf)
        numeStudenti = []
        for conventie in conventiiDeModificat:
            modify_conventie_input(conventie,nume,functie,email,phone,fax)
            numeStudenti.append(servStudInf.getOne(conventie.get_id()).name)
        mesaj = "Ati modificat cu succes conventiile urmatorilor studenti: "
        for nume in numeStudenti:
            mesaj = mesaj + str(nume) + "; "
        flash(mesaj)

        return render_template("cadruDidacticSupervizor/homeCadruDidacticSupervizor.html")
    else:
        return render_template("cadruDidacticSupervizor/conventieCadruDidacticSupervizor.html")


@cadru_didactic_supervizor.route('/cadru_didactic_supervizor_info', methods=["GET", "POST"])
def info():
    if request.method == "POST":
        from service.utility import get_supervisor_info_service
        from domain.supervisor_info import SupervisorInfo

        service = get_supervisor_info_service()

        name = request.form["name"]
        specialization = request.form["specialization"]

        service.add(SupervisorInfo(session["id"], name, specialization))
    return render_template("cadruDidacticSupervizor/infoCadruDidacticSupervizor.html")

@cadru_didactic_supervizor.route('/cadru_didactic_supervizor', methods=["GET"])
def home():
    if verify_role(5) == 0:
        return  redirect(url_for(get_home_route()))
    return render_template("cadruDidacticSupervizor/homeCadruDidacticSupervizor.html")


#todo: implement general data for cadruDidacticSuperizor