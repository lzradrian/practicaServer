from flask import Blueprint, redirect, flash, render_template, session, request, url_for

from controller.helpers.authorize import verify_role
from repository.conventie_repository import ConventieRepository
from repository.acord_repository import AcordRepository
from repository.company_info_repository import CompanyInfoRepository
from repository.user_repository import UserRepository
from service.conventie_service import ConventieService
from service.acord_service import AcordService
from service.user_service import UserService
from service.company_info_service import CompanyInfoService

responsabil_firma = Blueprint('responsabil_firma', __name__)


def modify_conventie_input_txt(conventie, firm, city, street, number, phone, fax, email, code, account, banca,
                               representative,
                               function, address, hours, startInternshipDate, endInternshipDate, tutor, tutorfunction,
                               tutorphone, tutorfax, tutormail, date, signature):
    '''
    Actualizeaza contentul conventiei din baza de date cu datele primite ca parametrii
    '''
    content = conventie.get_content()
    replaced_content = ""

    from io import StringIO
    s = StringIO(content)
    for line in s:
        # todo: rezolve signature
        line = line.replace("CompanyName Name", "CompanyName " + firm)
        line = line.replace("CompanyCity City", "CompanyCity " + city)
        line = line.replace("CompanyStreet Street", "CompanyStreet  " + street)
        line = line.replace("CompanyStreetNo StreetNo", "CompanyStreetNo " + number)
        line = line.replace("CompanyFax Fax", "CompanyFax " + fax)
        line = line.replace("CompanyPhone 1234567890", "CompanyPhone " + phone)
        line = line.replace("CompanyEmail Email", "CompanyEmail " + email)
        line = line.replace("CompanyFiscalCode FiscalCode", "CompanyFiscalCode " + code)
        line = line.replace("CompanyAccount Account", "CompanyAccount " + account)
        line = line.replace("CompanyBank Bank", "CompanyBank " + banca)
        line = line.replace("CompanyRepresentative RepresentativeName", "CompanyRepresentative " + representative)
        line = line.replace("CompanyRepresentativeRole Role", "CompanyRepresentativeRole " + function)
        line = line.replace("CompanyAddress Address", "CompanyAddress " + address)
        line = line.replace("InternshipLength 120", "InternshipLength " + hours)
        line = line.replace("InternshipStartDate 2020.10.10", "InternshipStartDate " + startInternshipDate)
        line = line.replace("InternshipEndDate 2021.10.10", "InternshipEndDate " + endInternshipDate)
        line = line.replace("TutorName Name", "TutorName " + tutor)
        line = line.replace("TutorPhone Phone", "TutorPhone " + tutorphone)
        line = line.replace("TutorFax Fax", "TutorFax " + tutorfax)
        line = line.replace("TutorEmail Email", "TutorEmail " + tutormail)
        line = line.replace("TutorFunction Function", "TutorFunction " + tutorfunction)
        # todo: articolul 12 nu este implementat. Este necesar?
        line = line.replace("ConventionSignDate Date", "ConventionSignDate " + date)
        line = line.replace("SignRepresentativeName Name", "SignRepresentativeName " + representative)
        line = line.replace("SignRepresentativeDate Date", "SignRepresentativeDate " + date)
        line = line.replace("AcknowledgementSupervisorName Name", "AcknowledgementSupervisorName " + representative)
        line = line.replace("SignRepresentativeDate Date", "SignRepresentativeDate " + date)
        line = line.replace("AcknowledgementTutorName Name", "AcknowledgementTutorName " + tutor)
        line = line.replace("AcknowledgementTutorFunction Function", "AcknowledgementTutorFunction " + tutorfunction)
        line = line.replace("AcknowledgementTutorDate Date", "AcknowledgementTutorDate " + date)

        replaced_content = replaced_content + line

    conventie.set_content(replaced_content)
    conventie.set_completedByFirmaResponsabil(True)

    conventieRepo = ConventieRepository()
    conventieService = ConventieService(conventieRepo)
    conventieService.update(conventie)
    from controller.helpers.pdfTools import create_pdf_from_conventie
    create_pdf_from_conventie("ConventiePractica.pdf", "output.pdf", conventie)


@responsabil_firma.route('/conventie_responsabil_firma', methods=["POST", "GET"])
def conventie():
    if request.method == "POST":

        # todo: sa poata modifica doar conventiile studentilor de la firma lui
        conventieRepo = ConventieRepository()
        conventieService = ConventieService(conventieRepo)
        conventii = conventieService.getAll()
        conventieDeModificat = None
        for conventie in conventii:
            if conventie.get_completedByStudent() == True and conventie.get_completedByFirmaResponsabil() == False:
                conventieDeModificat = conventie
                break

        if conventieDeModificat == None:
            print("Nu s-a gasit o conventie de modificat")
            return render_template("firmaResponsabil/conventieResponsabilFirma.html")

        # todo: put real data from forms
        firm = request.form["firm"]
        city = request.form["city"]
        street = request.form["street"]
        number = request.form["number"]
        phone = request.form["phone"]
        fax = request.form["fax"]
        email = request.form["email"]
        code = request.form["code"]
        account = request.form["account"]
        banca = request.form["banca"]
        representative = request.form["representative"]
        function = request.form["function"]
        address = request.form["address"]
        hours = request.form["hours"]
        startInternshipDate = request.form["startInternshipDate"]
        endInternshipDate = request.form["endInternshipDate"]
        tutor = request.form["tutor"]
        tutorfunction = request.form["tutorfunction"]
        tutorphone = request.form["tutorphone"]
        tutorfax = request.form["tutorfax"]
        tutormail = request.form["tutormail"]
        date = request.form["date"]
        signature = request.form["signature"]
        modify_conventie_input_txt(conventieDeModificat, firm, city, street, number, phone, fax, email, code, account,
                                   banca, representative,
                                   function, address, hours, startInternshipDate, endInternshipDate, tutor,
                                   tutorfunction, tutorphone, tutorfax, tutormail, date, signature)

        return render_template("firmaResponsabil/conventieResponsabilFirma.html")
    else:
        return render_template("firmaResponsabil/conventieResponsabilFirma.html")


def create_acord(accordYear, noHours, accordSignDate, companyName, companyCity, companyStreet, companyStreetNo,
                 companyPhone, fax, companyFiscalCode, companyBank, companyIBAN, companyLegalRepresentative,
                 nrOfStudents, noStudents1, noStudents2, specialization1, specialization2, faculty1, faculty2):
    import os
    dir_location = os.getcwd()
    while dir_location[-1] != "\\":
        dir_location = dir_location[:-1]
    dir_location_input = dir_location[:-1] + "\\forms\\acord_input.txt"

    file = open(dir_location_input, "r")
    replaced_content = ""

    for line in file:
        line = line.strip()
        # todo: rezolve signature
        line = line.replace("AccordYear 2020-2021", "AccordYear " + accordYear)
        line = line.replace("InternshipLenghtDays 50", "InternshipLenghtDays " + noHours)  # hours
        line = line.replace("AccordSignDate 10.10.2020", "AccordSignDate  " + accordSignDate)
        line = line.replace("CompanyName Company", "CompanyName " + companyName)
        line = line.replace("CompanyCity Cluj-Napoca", "CompanyCity " + companyCity)
        line = line.replace("CompanyStreet Street", "CompanyStreet " + companyStreet)
        line = line.replace("CompanyStreetNo 20db", "CompanyStreetNo " + companyStreetNo)
        line = line.replace("CompanyPhone 1234567890", "CompanyPhone " + companyPhone)
        line = line.replace("CompanyFax Fax", "CompanyFax " + fax)
        line = line.replace("CompanyFiscalCode Code", "CompanyFiscalCode " + companyFiscalCode)
        line = line.replace("CompanyBank Bank", "CompanyBank " + companyBank)
        line = line.replace("CompanyIBAN IBAN", "CompanyIBAN " + companyIBAN)
        line = line.replace("CompanyLegalRepresentative Representative",
                            "CompanyLegalRepresentative " + companyLegalRepresentative)
        line = line.replace("TotalNoStudents 20", "TotalNoStudents " + nrOfStudents)
        line = line.replace("NoStudents1 10", "NoStudents1 " + noStudents1)
        line = line.replace("NoStudents2 10", "NoStudents2 " + noStudents2)
        line = line.replace("Specialization1 Informatica", "Specialization1 " + specialization1)
        line = line.replace("Specialization2 Matematica-Informatica", "Specialization2 " + specialization2)
        line = line.replace("Faculty2 Matematica-Informatica", "Faculty2 " + faculty2)
        line = line.replace("Faculty1 Matematica-Informatica", "Faculty1 " + faculty1)

        replaced_content = replaced_content + line + "\n"
    file.close()

    from domain.acordPractica import AcordPractica
    acordRepo = AcordRepository()
    acordServ = AcordService(acordRepo)
    acord = AcordPractica(replaced_content)
    acord.set_completedByFirmaReprezentant(True)

    acordServ.add(acord)

    from controller.helpers.pdfTools import create_pdf_from_conventie
    create_pdf_from_conventie("AcordPractica.pdf", "output.pdf", acord)


@responsabil_firma.route('/acord_responsabil_firma', methods=["POST", "GET"])
def acord():
    if verify_role(1) == 0:
        return render_template("home.html")
    repoUser = UserRepository()
    serviceUser = UserService(repoUser)
    idOfCurrentUser = serviceUser.getOneByUsername(session["username"]).get_id()
    repoComp = CompanyInfoRepository()
    serviceComp = CompanyInfoService(repoComp)

    if request.method == "POST":
        company = serviceComp.getOne(idOfCurrentUser)
        accordYear = request.form["AccordYear"]
        noHours = request.form["InternshipLenghtDays"]
        accordSignDate = request.form["AccordSignDate"]

        companyName = company.get_name()
        companyCity = company.get_city()
        companyStreet = company.get_street()
        companyStreetNo = company.get_streetNo()
        companyPhone = company.get_phone()
        fax = company.get_fax()
        companyFiscalCode = company.get_fiscalCode()
        companyBank = company.get_bank()
        companyIBAN = company.get_iban()
        companyLegalRepresentative = company.get_legalRepresentative()

        nrOfStudents = request.form["TotalNoStudents"]
        noStudents1 = request.form["NoStudents1"]
        noStudents2 = request.form["NoStudents2"]
        specialization1 = request.form["Specialization1"]
        specialization2 = request.form["Specialization2"]
        faculty2 = request.form["Faculty2"]
        faculty1 = request.form["Faculty1"]

        create_acord(accordYear, noHours, accordSignDate, companyName, companyCity, companyStreet, companyStreetNo,
                     companyPhone, fax, companyFiscalCode, companyBank, companyIBAN, companyLegalRepresentative,
                     nrOfStudents, noStudents1, noStudents2, specialization1, specialization2, faculty1, faculty2)

        return render_template("firmaResponsabil/acordResponsabilFirma.html")
    else:
        try:
            company = serviceComp.getOne(idOfCurrentUser)
        except:
            flash("Trebuie sa introduceti mai intai datele firmei.")
            return redirect(url_for("responsabil_firma.home"))
        return render_template("firmaResponsabil/acordResponsabilFirma.html")


@responsabil_firma.route('/responsabil_firma_date_firma', methods=["GET", "POST"])
def date_firma():
    if verify_role(1) == 0:
        return render_template("home.html")
    if request.method == "POST":
        repoUser = UserRepository()
        serviceUser = UserService(repoUser)
        idOfCurrentUser = serviceUser.getOneByUsername(session["username"]).get_id()

        companyName = request.form["CompanyName"]
        companyCity = request.form["CompanyCity"]
        companyStreet = request.form["CompanyStreet"]
        companyStreetNo = request.form["CompanyStreetNo"]
        companyPhone = request.form["CompanyPhone"]
        companyFax = request.form["CompanyFax"]
        companyFiscalCode = request.form["CompanyFiscalCode"]
        companyBank = request.form["CompanyBank"]
        companyIBAN = request.form["CompanyIBAN"]
        companyLegalRepresentative = request.form["CompanyLegalRepresentative"]

        from domain.company_info import CompanyInfo
        companyInfo = CompanyInfo(idOfCurrentUser, companyLegalRepresentative, companyName, companyCity, companyStreet,
                                  companyStreetNo, companyPhone, companyFax
                                  , companyFiscalCode, companyBank, companyIBAN)
        repoComp = CompanyInfoRepository()
        serviceComp = CompanyInfoService(repoComp)
        try:
            serviceComp.add(companyInfo)
        except:  # nu s-a putut adauga, deci deja exista, caz in care il updatam.
            serviceComp.update(companyInfo)

        flash("Ati completat cu succes datele firmei!")
        return redirect(url_for("responsabil_firma.home"))
    else:
        return render_template("firmaResponsabil/dateGeneraleFirma.html")


@responsabil_firma.route('/responsabil_firma', methods=["GET"])
def home():
    if verify_role(1) == 0:
        return render_template("home.html")
    return render_template("firmaResponsabil/homeResponsabilFirma.html")
