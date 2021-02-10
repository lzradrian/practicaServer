from flask import Blueprint, redirect, flash, render_template, session, request, url_for

from controller.helpers.authorize import verify_role, get_home_route
from repository.conventie_repository import ConventieRepository
from service.conventie_service import ConventieService
from repository.student_info_repository import StudentInfoRepository
from service.student_info_service import StudentInfoService
from controller.helpers.pdfTools import create_pdf_from_files_and_doc
decan = Blueprint('decan', __name__)


def modify_conventie_input(conventie,signature):
    '''
    Actualizeaza contentul conventiei din baza de date cu datele primite ca parametrii
    '''
    content = conventie.get_content()
    replaced_content = ""
    from datetime import date, datetime
    from io import StringIO
    s = StringIO(content)
    for line in s:
        line = line.replace("SignUniversityDate Date", "SignUniversityDate " + str(date.today()))
        if "DecanSignature" in line:
            line= "DecanSignature "+signature+"\n"
        replaced_content = replaced_content + line

    conventie.set_content(replaced_content)
    conventie.set_completedByDecan(True)

    conventieRepo = ConventieRepository()
    conventieService = ConventieService(conventieRepo)
    conventieService.update(conventie)

    return conventie

@decan.route('/conventie_decan', methods=["POST", "GET"])
def conventie():
    repoStudInf = StudentInfoRepository()
    servStudInf = StudentInfoService(repoStudInf)

    conventieRepo = ConventieRepository()
    conventieService = ConventieService(conventieRepo)
    conventii = conventieService.getAll()
    conventiiDeModificat =[]
    numeStudenti = []

    for conventie in conventii:
        if conventie.get_completedByStudent() == True and conventie.get_completedByFirmaResponsabil() == True and conventie.get_completedByFirmaTutori() == True and conventie.get_completedByCadruDidacticSupervizor() == True and conventie.get_completedByDecan() == False:
            conventiiDeModificat.append(conventie)
    if request.method == "POST":
        signature = request.form["signature"]

        for conventie in conventiiDeModificat:
                conventieDeModificat = conventie
                conventieDeModificat = modify_conventie_input(conventieDeModificat,signature)
                infoStud = servStudInf.getOne(conventie.get_id())
                numeStud=infoStud.name
                numeStudenti.append(numeStud)
                mailSubject = infoStud.specialization +","+infoStud.name +",2021,"+"C"  #sectie nume promotie tipdoc(A,C,R,E)
                file_name= infoStud.name+"Conventie.pdf"
                create_pdf_from_files_and_doc("ConventiePractica.pdf", file_name, conventieDeModificat,mailSubject)

        mesaj = "Ati semnat cu succes conventiile urmatorilor studenti: "
        for nume in numeStudenti:
            mesaj = mesaj + str(nume) + "; "
        flash(mesaj)

        return render_template("decan/homeDecan.html")
    else:
        if len(conventiiDeModificat)==0:
            flash("Nu s-au gasit conventii de modificat")
            return render_template("decan/homeDecan.html")

        return render_template("decan/conventieDecan.html")


@decan.route('/decan', methods=["GET"])
def home():
    if verify_role(7) == 0:
        return  redirect(url_for(get_home_route()))
    return render_template("decan/homeDecan.html")
