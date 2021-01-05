from flask import Blueprint, redirect, flash, render_template, session, request, url_for

from controller.helpers.authorize import verify_role
from repository.conventie_repository import ConventieRepository
from service.conventie_service import ConventieService

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


@responsabil_firma.route('/management', methods=["GET", "POST"])
def management():
    from service.utility import get_internship_service, get_student_internship_service, get_user_service

    internship_service = get_internship_service()
    student_internship_service = get_student_internship_service()
    user_service = get_user_service()

    internship = internship_service.get_by_representative_id(session["id"])
    student_interships = student_internship_service.get_by_internship_id(internship.id)
    students = []
    for si in student_interships:
        students.append(user_service.getOne(si.student_id))
    headings = (("Nume Student",))
    student_names = tuple([(student.username,) for student in students])
    return render_template("firmaResponsabil/managementResponsabilFirma.html", headings=headings, data=student_names)

@responsabil_firma.route('/add_student', methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        from service.utility import get_internship_service, get_student_internship_service,\
            get_user_service, get_student_info_service
        from domain.student_internship import StudentInternship

        name = request.form["name"]
        year = request.form["year"]
        group = request.form["group"]

        internship_service = get_internship_service()
        student_internship_service = get_student_internship_service()
        student_info_service = get_student_info_service()

        try:
            student_info = student_info_service.get_by_identifiers(name, year, group)
            internship = internship_service.get_by_representative_id(session["id"])
            student_internship_service.add(StudentInternship(None, internship.id, student_info.student_id))
        except ValueError:
            return render_template("firmaResponsabil/managementResponsabilFirma.html", error="No student with given identifiers could be found!")
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
