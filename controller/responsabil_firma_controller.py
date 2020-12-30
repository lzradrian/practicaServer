from flask import Blueprint , redirect,flash,render_template,session,request,url_for

from controller.helpers.authorize import verify_role
from repository.conventie_repository import ConventieRepository
from service.conventie_service import ConventieService

responsabil_firma = Blueprint('responsabil_firma',__name__)


def modify_conventie_input_txt(conventie,nume):
    '''
    Actualizeaza contentul conventiei din baza de date cu datele primite ca parametrii
    '''
    content = conventie.get_content()
    replaced_content = ""

    from io import StringIO
    s = StringIO(content)
    for line in s:
        line = line.replace("CompanyName Name", "CompanyName " + nume)
        line = line.replace("CompanyCity City", "TutorPhone " + nume)
        line = line.replace("CompanyStreet Street", "TutorFax  " + nume)
        line = line.replace("CompanyStreetNo StreetNo", "TutorEmail " + nume)
        line = line.replace("CompanyFax Fax", "TutorFunction " + nume)
        line = line.replace("CompanyEmail Email", "CompanyEmail " + nume)
        line = line.replace("CompanyFiscalCode FiscalCode", "CompanyFiscalCode " + nume)
        line = line.replace("CompanyAccount Account", "CompanyAccount " + nume)
        line = line.replace("CompanyBank Bank", "CompanyBank " + nume)
        line = line.replace("CompanyRepresentative RepresentativeName", "CompanyRepresentative " + nume)
        line = line.replace("CompanyRepresentativeRole Role", "CompanyRepresentativeRole " + nume)
        line = line.replace("CompanyAddress Address", "CompanyAddress " + nume)
        line = line.replace("InternshipLength 120", "InternshipLength " + nume)
        line = line.replace("InternshipStartDate 2020.10.10", "InternshipStartDate " + nume)
        line = line.replace("InternshipEndDate 2021.10.10", "InternshipEndDate " + nume)
        #todo: alte date

        replaced_content = replaced_content + line

    conventie.set_content(replaced_content)
    conventie.set_completedByFirmaResponsabil(True)

    conventieRepo = ConventieRepository()
    conventieService = ConventieService(conventieRepo)
    conventieService.update(conventie)


@responsabil_firma.route('/conventie_responsabil_firma', methods=["POST", "GET"])
def conventie():
    if request.method == "POST":

        conventieRepo = ConventieRepository()
        conventieService = ConventieService(conventieRepo)
        conventii = conventieService.getAll()
        conventieDeModificat = None
        for conventie in conventii:
            if conventie.get_completedByStudent()==True and conventie.get_completedByFirmaResponsabil()==False:
                conventieDeModificat=conventie
                break

        if conventieDeModificat==None:
            print("Nu s-a gasit o conventie de modificat")
            return render_template("conventieResponsabilFirma.html")

        # todo: put real data from forms
        #numeFirma = request.form["numeFirma"]
        nume = "numeResponsabilFirma"

        modify_conventie_input_txt(conventieDeModificat,nume)


        return render_template("conventieResponsabilFirma.html")
    else:
        return render_template("conventieResponsabilFirma.html")


@responsabil_firma.route('/responsabil_firma',methods=["GET"])
def home():

    if verify_role(1) == 0:
        return render_template("home.html")
    return render_template("homeResponsabilFirma.html")

