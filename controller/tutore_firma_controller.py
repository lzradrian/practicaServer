from flask import Blueprint, redirect, flash, render_template, session, request, url_for

from controller.helpers.authorize import verify_role
from repository.conventie_repository import ConventieRepository
from service.conventie_service import ConventieService

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
        line = line.replace("AcknowledgementTutorName Name", "AcknowledgementTutorName " + name)
        line = line.replace("AcknowledgementSupervisorFunction Function",
                            "AcknowledgementSupervisorFunction " + function)
        # todo: replace signature (did not find in conventie_input.txt)
        replaced_content = replaced_content + line

    conventie.set_content(replaced_content)
    conventie.set_completedByFirmaTutori(True)

    conventieRepo = ConventieRepository()
    conventieService = ConventieService(conventieRepo)
    conventieService.update(conventie)


@tutore_firma.route('/conventie_tutore_firma', methods=["POST", "GET"])
def conventie():
    if request.method == "POST":

        # todo: sa poata modifica doar conventiile studentilor pe care ii coordoneaza
        conventieRepo = ConventieRepository()
        conventieService = ConventieService(conventieRepo)
        conventii = conventieService.getAll()
        conventieDeModificat = None
        for conventie in conventii:
            if conventie.get_completedByStudent() == True and conventie.get_completedByFirmaTutori() == False:
                conventieDeModificat = conventie
                break

        if conventieDeModificat == None:
            print("Nu s-a gasit o conventie de modificat")
            return render_template("firmaTutore/conventieTutoreFirma.html")

        tutorname = request.form["tutorname"]
        tutorfunction = request.form["tutorfunction"]
        signature = request.form["signature"]

        modify_conventie_input(conventieDeModificat, tutorname, tutorfunction, signature)

        return render_template("firmaTutore/conventieTutoreFirma.html")
    else:
        return render_template("firmaTutore/conventieTutoreFirma.html")


@tutore_firma.route('/tutore_firma', methods=["GET"])
def home():
    if verify_role(2) == 0:
        return render_template("home.html")
    return render_template("firmaTutore/homeTutoreFirma.html")
