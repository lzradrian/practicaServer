from flask import Blueprint, redirect, flash, render_template, session, request, url_for

from controller.helpers.authorize import verify_role
from repository.conventie_repository import ConventieRepository
from service.conventie_service import ConventieService

cadru_didactic_supervizor = Blueprint('cadru_didactic_supervizor', __name__)


def modify_conventie_input(conventie, nume):
    '''
    Actualizeaza contentul conventiei din baza de date cu datele primite ca parametrii
    '''
    content = conventie.get_content()
    replaced_content = ""

    from io import StringIO
    s = StringIO(content)
    for line in s:
        line = line.replace("SupervisorFunction Function", "SupervisorFunction " + nume)
        line = line.replace("SupervisorName Name", "SupervisorName " + nume)
        line = line.replace("SupervisorEmail Email", "SupervisorEmail " + nume)
        line = line.replace("SupervisorPhone Phone", "SupervisorPhone " + nume)
        line = line.replace("SupervisorFax Fax", "SupervisorFax " + nume)
        # todo: alte date

        replaced_content = replaced_content + line

    conventie.set_content(replaced_content)
    conventie.set_completedByCadruDidacticSupervizor(True)

    conventieRepo = ConventieRepository()
    conventieService = ConventieService(conventieRepo)
    conventieService.update(conventie)


@cadru_didactic_supervizor.route('/conventie_cadru_didactic_supervizor', methods=["POST", "GET"])
def conventie():
    if request.method == "POST":

        # todo: sa poata modifica doar conventiile studentilor pe care ii supervizeaza
        conventieRepo = ConventieRepository()
        conventieService = ConventieService(conventieRepo)
        conventii = conventieService.getAll()
        conventieDeModificat = None
        for conventie in conventii:
            if conventie.get_completedByStudent() == True and conventie.get_completedByFirmaResponsabil() == True and conventie.get_completedByFirmaTutori() == True and conventie.get_completedByCadruDidacticSupervizor() == False:
                conventieDeModificat = conventie
                break

        if conventieDeModificat == None:
            print("Nu s-a gasit o conventie de modificat")
            return render_template("cadruDidacticSupervizor/conventieCadruDidacticSupervizor.html")

        # todo: put real data from forms
        # numeFirma = request.form["numeFirma"]
        nume = "CADRUDIDACTICSUPERVIZOR"

        modify_conventie_input(conventieDeModificat, nume)

        return render_template("cadruDidacticSupervizor/conventieCadruDidacticSupervizor.html")
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
