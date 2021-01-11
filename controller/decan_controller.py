from flask import Blueprint, redirect, flash, render_template, session, request, url_for

from controller.helpers.authorize import verify_role, get_home_route
from repository.conventie_repository import ConventieRepository
from service.conventie_service import ConventieService

decan = Blueprint('decan', __name__)


def modify_conventie_input(conventie, nume):
    '''
    Actualizeaza contentul conventiei din baza de date cu datele primite ca parametrii
    '''
    content = conventie.get_content()
    replaced_content = ""

    from io import StringIO
    s = StringIO(content)
    for line in s:
        # line = line.replace("SupervisorFunction Function", "SupervisorFunction " + nume)
        replaced_content = replaced_content + line

    conventie.set_content(replaced_content)
    conventie.set_completedByDecan(True)

    conventieRepo = ConventieRepository()
    conventieService = ConventieService(conventieRepo)
    conventieService.update(conventie)


@decan.route('/conventie_decan', methods=["POST", "GET"])
def conventie():
    if request.method == "POST":

        conventieRepo = ConventieRepository()
        conventieService = ConventieService(conventieRepo)
        conventii = conventieService.getAll()
        conventieDeModificat = None

        for conventie in conventii:
            if conventie.get_completedByStudent() == True and conventie.get_completedByFirmaResponsabil() == True and conventie.get_completedByFirmaTutori() == True and conventie.get_completedByCadruDidacticSupervizor() == True and conventie.get_completedByDecan() == False:
                conventieDeModificat = conventie
                break

        if conventieDeModificat == None:
            print("Nu s-a gasit o conventie de modificat")
            return render_template("decan/conventieDecan.html")

        # todo: put real data from forms
        # numeFirma = request.form["numeFirma"]
        nume = "DECAN"

        modify_conventie_input(conventieDeModificat, nume)

        from controller.helpers.pdfTools import create_pdf_from_files_and_doc
        create_pdf_from_files_and_doc("ConventiePractica.pdf", "output.pdf", conventieDeModificat)

        return render_template("decan/conventieDecan.html")
    else:
        return render_template("decan/conventieDecan.html")


@decan.route('/decan', methods=["GET"])
def home():
    if verify_role(7) == 0:
        return  redirect(url_for(get_home_route()))
    return render_template("decan/homeDecan.html")
