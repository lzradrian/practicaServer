from flask import Blueprint, redirect, flash, render_template, session, request, url_for

from controller.helpers.authorize import verify_role, get_home_route
from repository.conventie_repository import ConventieRepository
from repository.acord_repository import AcordRepository
from repository.company_info_repository import CompanyInfoRepository
from repository.user_repository import UserRepository
from service.conventie_service import ConventieService
from service.acord_service import AcordService
from service.user_service import UserService
from service.company_info_service import CompanyInfoService
from service.conventie_service import ConventieService

responsabil_firma = Blueprint('responsabil_firma', __name__)


def modify_conventie_input(conventie, firm, city, street, number, phone, fax, email, code, account, banca,
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
    #from controller.helpers.pdfTools import create_pdf_from_files_and_doc
    #create_pdf_from_files_and_doc("ConventiePractica.pdf", "output.pdf", conventie)


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
        modify_conventie_input(conventieDeModificat, firm, city, street, number, phone, fax, email, code, account,
                               banca, representative,
                               function, address, hours, startInternshipDate, endInternshipDate, tutor,
                               tutorfunction, tutorphone, tutorfax, tutormail, date, signature)

        return render_template("firmaResponsabil/conventieResponsabilFirma.html")
    else:
        return render_template("firmaResponsabil/conventieResponsabilFirma.html")


def get_associated_students():
    from service.utility import get_internship_service, get_student_internship_service, get_user_service,\
        get_student_info_service

    internship_service = get_internship_service()
    student_internship_service = get_student_internship_service()
    user_service = get_user_service()
    student_info_service = get_student_info_service()

    internship = internship_service.get_by_representative_id(session["id"])
    #student_interships = student_internship_service.get_by_internship_id(internship.id)
    student_interships = student_internship_service.getAll()
    students = []
    for si in student_interships:
        students.append(student_info_service.getOne(si.student_id))
    headings = (("Nume Student", "Grupa", "An"))
    student_info = tuple([(student.name, student.group, student.year) for student in students])
    return headings, student_info

def get_supervisors():
    from service.utility import get_user_service, get_supervisor_info_service

    user_service = get_user_service()
    supervisor_info_service = get_supervisor_info_service()

    supervisors = user_service.filter_by_role(5)
    supervisor_infos = [supervisor_info_service.getOne(s.id) for s in supervisors]
    return list(zip([s.id for s in supervisors], [si.name for si in supervisor_infos]))


def get_tutors():
    from service.utility import get_user_service, get_tutor_info_service

    user_service = get_user_service()
    tutor_info_service = get_tutor_info_service()

    tutors = user_service.filter_by_role(2)
    tutor_infos = [tutor_info_service.getOne(t.id) for t in tutors]
    return list(zip([t.id for t in tutors], [ti.name for ti in tutor_infos]))

@responsabil_firma.route('/management', methods=["GET", "POST"])
def management():
    headings, student_info = get_associated_students()
    supervisors = get_supervisors()
    tutors = get_tutors()
    return render_template("firmaResponsabil/managementResponsabilFirma.html", headings=headings, data=student_info,
                           supervisors=supervisors, tutors=tutors)


@responsabil_firma.route('/add_student', methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        from service.utility import get_internship_service, get_student_internship_service,\
            get_user_service, get_student_info_service, get_tutor_info_service,\
            get_supervisor_info_service
        from domain.student_internship import StudentInternship

        headings, student_names = get_associated_students()

        name = request.form["name"]
        tutor_name = request.form["tutor_name"]
        supervisor_name = request.form["supervisor_name"]
        year = request.form["year"]
        group = request.form["group"]

        internship_service = get_internship_service()
        student_internship_service = get_student_internship_service()
        student_info_service = get_student_info_service()
        tutor_info_service = get_tutor_info_service()
        supervisor_info_service = get_supervisor_info_service()

        try:
            tutor_info = tutor_info_service.get_by_name(tutor_name)
            supervisor_info = supervisor_info_service.get_by_name(supervisor_name)
            student_info = student_info_service.get_by_identifiers(name, year, group)
            internship = internship_service.get_by_representative_id(session["id"])
            student_internship_service.add(StudentInternship(internship.id, student_info.id, tutor_info.id, supervisor_info.id))
        except ValueError:
            return render_template("firmaResponsabil/managementResponsabilFirma.html", headings=headings, student_names=student_names, error="No student with given identifiers could be found!")
    return render_template("firmaResponsabil/homeResponsabilFirma.html")


@responsabil_firma.route('/start_internship', methods=["GET", "POST"])
def start_internship():
    if request.method == "POST":
        from repository.internship_repository import InternshipRepository
        from service.internship_service import InternshipService
        from domain.internship import Internship
        from datetime import datetime

        repo = InternshipRepository()
        service = InternshipService(repo)

        responsabil_id = session["id"]
        year = request.form["year"]
        start_date = datetime.strptime(request.form["start_date"], '%Y-%m-%d')
        end_date = datetime.strptime(request.form["end_date"], '%Y-%m-%d')

        service.add(Internship(0, responsabil_id, year, start_date, end_date))

    return render_template("firmaResponsabil/practicaResponsabilFirma.html")

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

    from controller.helpers.pdfTools import create_pdf_from_files_and_doc
    create_pdf_from_files_and_doc("AcordPractica.pdf", "output.pdf", acord)


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
    import datetime
    from repository.internship_repository import InternshipRepository
    from service.internship_service import InternshipService

    repo = InternshipRepository()
    service = InternshipService(repo)

    active = False

    try:
        internship = service.get_by_representative_id(session["id"])
        active = True
    except ValueError:
        pass

    if verify_role(1) == 0:
        return render_template("home.html")
    year = datetime.datetime.now().year
    return render_template("firmaResponsabil/homeResponsabilFirma.html", year=year, active=active)
