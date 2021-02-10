from flask import Blueprint, redirect, flash, render_template, session, request, url_for, send_from_directory, Response

from controller.helpers.authorize import verify_role, auth_required_with_role, get_home_route
from controller.helpers.pdfTools import create_pdf_from_dic, create_pdf_from_files_and_doc
from repository.conventie_repository import ConventieRepository
from service.conventie_service import ConventieService
from repository.student_info_repository import StudentInfoRepository
from service.student_info_service import StudentInfoService

student = Blueprint('student', __name__)

def create_conventie_input(name, country, city, street, number, apartment, county, phone, email, cnp, series, id,
                           birthdate, birthcity, function, year, group, specialty, lineOfStudy, date,
                           signature):
    import os
    dir_location = os.getcwd()
    while dir_location[-1] != "\\":
        dir_location = dir_location[:-1]
    dir_location_input = dir_location[:-1] + "\\forms\\conventie_input.txt"
    k = 0
    file = open(dir_location_input, "r")
    replaced_content = ""
    for line in file:
        line = line.strip()
        if "StudentName" in line and k==0:
            k=k+1
            line = "StudentName " + name
        if "StudentCity" in line:
            line = "StudentCity " + city
        if "StudentStreet" in line:
            line = "StudentStreet " +street
        if "StudentPNC" in line:
            line = "StudentPNC " + cnp
        if "StudentDateOfBirth" in line:
            line = "StudentDateOfBirth " + birthdate
        if "StudentPhone" in line:
            line = "StudentPhone " +phone
        if "StudentEmail" in line:
            line = "StudentEmail " +email
        if "StudentCounty" in line:
            line = "StudentCounty " + county
        if "StudentApartment" in line:
            line = "StudentApartment " + apartment
        if "StudentStudyLine" in line:
            line = "StudentStudyLine " + lineOfStudy
        if "StudentRole" in line:
            line = "StudentRole " + function
        if "StudentBirthLocation" in line:
            line = "StudentBirthLocation " + birthcity
        if "StudentSpecialization" in line:
            line = "StudentSpecialization " + specialty
        if "StudentNationality" in line:
            line = "StudentNationality " + country
        if "StudentGroup" in line:
            line = "StudentGroup " + group
        if "StudentYear" in line:
            line = "StudentYear " + str(year)
        if "StudentICSeries" in line:
            line = "StudentICSeries " + series
        if "StudentStreetNo" in line:
            line = "StudentStreetNo " + number
        if "StudentICNo" in line:
            line = "StudentICNo " + id
        if "StudentNationality" in line:
            line = "StudentNationality " + country
        if "SignStudentDate" in line:
            line = "SignStudentDate " + date
        if "StudentSignature" in line:
            line = "StudentSignature " + signature
        if "SignStudentName" in line:
            line = "SignStudentName "+name
        replaced_content = replaced_content + line + "\n"


    file.close()

    from domain.conventie_input import ConventieInput
    conventieRepo = ConventieRepository()
    conventieService = ConventieService(conventieRepo)
    conventie = ConventieInput(session["id"], replaced_content)
    conventie.set_completedByStudent(True)
    try:
        #flash("Ati modificat datele conventiei cu succes!")
        conventieService.update(conventie)
    except:
        flash("Ati completat conventia cu succes!")
        conventieService.add(conventie)

    conv = conventieService.getOne(session["id"])
    blobContent = create_pdf_from_files_and_doc("ConventiePractica.pdf", "conventie.pdf", conv,None)
    conv.set_blobContent(blobContent)
    conventieService.update(conv)


@student.route("/student_conventie", methods=["POST", "GET"])
def conventie():
    if request.method == "POST":
        from domain.student_info import StudentInfo
        from domain.conventie_student_file import fields
        from datetime import date, datetime
        studentInfoRepo = StudentInfoRepository()
        studentInfoServ = StudentInfoService(studentInfoRepo)
        info = studentInfoServ.getOne(session["id"])

        name = info.name
        cnp = info.pnc
        group = info.group
        specialty = info.specialization
        year = info.year
        function = info.student_function
        line = info.study_line
        try:
            country = request.form["nationality"]
            city = request.form["city"]
            street = request.form["street"]
            number = request.form["number"]
            apartment = request.form["apartment"]
            county = request.form["county"]
            phone = request.form["phone"]
            email = request.form["email"]
            series = request.form["series"]
            id = request.form["id"]
            birthdate = request.form["birthdate"]
            birthcity = request.form["birthlocation"]
            date = str(date.today())
            signature = request.form["signature"]
        except:
            flash("Cel putin un camp nu este completat!")
            return redirect(url_for("student_conventie.home"))

        create_conventie_input(name, country, city, street, number, apartment, county, phone, email, cnp, series,
                               id, birthdate, birthcity, function, year, group, specialty, line, date,
                               signature)

        return redirect(url_for("student.home"))
    else:
        studentInfoRepo = StudentInfoRepository()
        studentInfoServ = StudentInfoService(studentInfoRepo)
        try:
            info = studentInfoServ.getOne(session["id"])
            #todo: campurile sa fie completate cu valorile introduse anterior
            return render_template("student/conventieStudent.html")
        except:
            flash("Completati datele generale inainte de completarea conventiei!")
            #return render_template("student/homeStudent.html")
            return redirect(url_for("student.home"))


@student.route('/download_conventie', methods=["GET"])
def download_conventie():
    conventieRepo = ConventieRepository()
    conventieService = ConventieService(conventieRepo)
    try:
        conventie = conventieService.getOne(session["id"])
        content = conventie.get_blobContent()

        return Response(content, mimetype="application/pdf",
                        headers={"Content-disposition": "attachment; " "filename=conventie.pdf"})
    except:
        flash("Completati mai intai conventia!")
        return redirect(url_for("student.home"))



@student.route("/student_company_declaration", methods=["POST", "GET"])
def student_company_declaration():
    if request.method == "POST":
        from repository.student_info_repository import StudentInfoRepository
        from service.student_info_service import StudentInfoService
        from domain.student_info import StudentInfo
        from datetime import date, datetime
        from domain.declaratie_firma_file import fields
        from controller.helpers.pdfTools import create_pdf_from_dic
        from service.utility import get_declaratie_firma_service
        from domain.declaratie_firma import DeclaratieFirma

        repo = StudentInfoRepository()
        service = StudentInfoService(repo)
        declaratie_service = get_declaratie_firma_service()

        info = service.getOne(session["id"])
        date = str(date.today())
        params = [info.name, info.group, info.specialization, info.year,
                  request.form["interval"], date, request.form["address"],
                  request.form["firm"], request.form["coordinator"], request.form["signature"]]
        pair_input = dict(zip(fields.keys(), params))
        content = create_pdf_from_dic("DeclaratieActivitateFirma.pdf", "DeclaratieActivitateFirma-" + info.name + ".pdf", pair_input)
        try:
            declaratie_found = declaratie_service.get_with_student_id(session["id"])
            declaratie_service.update(DeclaratieFirma(None, session["id"], datetime.now(), content, False))
        except ValueError:
            declaratie_service.add(DeclaratieFirma(None, session["id"], datetime.now(), content, False))

        return redirect(url_for("student.home"))
    return render_template("student/declaratieFirmaStudent.html")


@student.route("/student_uni_declaration", methods=["POST", "GET"])
def student_uni_declaration():
    from service.utility import get_declaratie_ubb_service
    from controller.helpers.pdfTools import get_fields_from_pdf

    declaratie_service = get_declaratie_ubb_service()
    already_completed = False
    validated = False
    try:
        declaratie_found = declaratie_service.get_with_student_id(session["id"])
        already_completed = True
        validated = declaratie_found.checked
    except ValueError:
        pass

    if request.method == "POST":
        from repository.student_info_repository import StudentInfoRepository
        from service.student_info_service import StudentInfoService
        from domain.student_info import StudentInfo
        from datetime import date
        from domain.declaratie_ubb_file import fields
        from controller.helpers.pdfTools import create_pdf_from_dic
        from domain.declaratie_ubb import DeclaratieUBB
        from datetime import datetime
        import os

        repo = StudentInfoRepository()
        service = StudentInfoService(repo)

        info = service.getOne(session["id"])
        date = str(date.today())
        params = [info.name, info.group, info.specialization, info.year,
                  request.form["interval"], date, request.form["address"],
                  request.form["coordinator"], request.form["signature"]]
        pair_input = dict(zip(fields.keys(), params))
        content = create_pdf_from_dic("DeclaratieActivitateUBB.pdf","DeclaratieActivitateUBB-" + info.name + ".pdf", pair_input)

        if already_completed:
            declaratie_service.update(DeclaratieUBB(None, session["id"], datetime.now(), content, False))
        else:
            declaratie_service.add(DeclaratieUBB(None, session["id"], datetime.now(), content, False))

        return redirect(url_for("student.home"))
    else:
        return render_template("student/declaratieFacultateStudent.html", validated=validated)
    return render_template("student/declaratieFacultateStudent.html")

def get_checked_checkboxes(form):
    checkboxes = {}
    if form.get("transport_in_comun"):
        checkboxes["PublicTransport"] = 1
    if form.get("metrou"):
        checkboxes["Metro"] = 1
    if form.get("v_personal"):
        checkboxes["PersonalVehicle"] = 1
    if form.get("v_societate"):
        checkboxes["PublicVehicle"] = 1
    if form.get("avion"):
        checkboxes["Plane"] = 1
    if form.get("pieton"):
        checkboxes["AsPedestrian"] = 1
    if form.get("bicicleta"):
        checkboxes["Bicycle"] = 1
    if form.get("motocicleta"):
        checkboxes["Motorcycle"] = 1
    return checkboxes

@student.route("/student_traseu_declaration", methods=["POST", "GET"])
def student_traseu_declaration():
    from service.utility import get_declaratie_traseu_service
    from controller.helpers.pdfTools import get_fields_from_pdf

    declaratie_service = get_declaratie_traseu_service()
    already_completed = False
    try:
        declaratie_found = declaratie_service.getOne(session["id"])
        already_completed = True
    except ValueError:
        pass

    if already_completed:
        declaratie = declaratie_service.getOne(session["id"])
        fields = get_fields_from_pdf(declaratie.content)

    if request.method == "POST":
        from repository.student_info_repository import StudentInfoRepository
        from service.student_info_service import StudentInfoService
        from domain.student_info import StudentInfo
        from datetime import date
        from domain.declaratie_traseu_file import fields
        from controller.helpers.pdfTools import create_pdf_from_dic
        from domain.declaratie_traseu import DeclaratieTraseu
        from datetime import datetime
        import os

        repo = StudentInfoRepository()
        service = StudentInfoService(repo)

        info = service.getOne(session["id"])
        date = str(date.today())
        params = [info.name, info.pnc, info.faculty, info.group,
                  request.form["domiciliu_practica"], request.form["practica_domiciliu"],
                  request.form["practica"], request.form["data_practica1"], request.form["data_practica2"],
                  request.form["traseu_domiciliu_practica"], request.form["traseu_practica_domiciliu"],
                  date, request.form["signature"]]
        checkboxes = get_checked_checkboxes(request.form)
        pair_input = dict(zip(fields.keys(), params))
        pair_input.update(checkboxes)

        content = create_pdf_from_dic("DeclaratieDeTraseu.pdf", "DeclaratieDeTraseu-" + info.name + ".pdf", pair_input)

        if already_completed:
            declaratie_service.update(DeclaratieTraseu(session["id"], datetime.now(), content, False))
        else:
            declaratie_service.add(DeclaratieTraseu(session["id"], datetime.now(), content, False))

        return redirect(url_for("student.home"))

    return render_template("student/declaratieTraseuStudent.html")


@student.route("/student_info", methods=["POST", "GET"])
def student_info():
    from repository.student_info_repository import StudentInfoRepository
    from service.student_info_service import StudentInfoService
    from domain.student_info import StudentInfo

    repo = StudentInfoRepository()
    service = StudentInfoService(repo)

    student_id = session["id"]
    if request.method == "POST":
        name = request.form["name"]
        pnc = request.form["pnc"]
        faculty = request.form["faculty"]
        student_function = request.form["student_function"]
        year = request.form["year"]
        group = request.form["group"]
        specialization = request.form["specialization"]
        study_line = request.form["specialization"]

        studentinfo = StudentInfo(student_id, name, pnc, student_function,
                               faculty, year, group, specialization, study_line)

        try:
            service.add(studentinfo)
            flash("Ati completat cu succes datele!")
        except ValueError:
            service.update(studentinfo)
            flash("Ati updatat cu succes datele!")
        return redirect(url_for("student.home"))
    else:
        try:
            info = service.getOne(student_id)
        except Exception as e:
            pass
        return render_template("student/infoStudent.html")


@student.route('/raport', methods=["POST", "GET"])
def raport():
    from service.utility import get_student_activity_service
    from domain.student_activity import StudentActivity

    service = get_student_activity_service()
    id = session["id"]

    if request.method == "POST":
        period = request.form["activity_date"]
        no_hours = request.form["no_hours"]
        description = request.form["description"]
        service.add(StudentActivity(None, id, period, int(no_hours), description))

        return redirect(url_for("student.raport"))

    headings = (("Perioada activitate", "Nr. ore", "Descriere activitate"))
    activities = service.get_all_with_student_id(id)
    activities = tuple([(activity.period, activity.no_hours, activity.description) for activity in activities])

    return render_template("student/raportStudent.html", headings=headings, data=activities)


@student.route('/download_declaratie_ubb', methods=["GET"])
def download_declaratie_ubb():
    from service.utility import get_declaratie_ubb_service

    service = get_declaratie_ubb_service()
    doc = service.get_with_student_id(session["id"])
    content = doc.content

    return Response(content, mimetype="application/pdf", headers={"Content-disposition": "attachment; "
                                                                                         "filename=declaratie.pdf"})


@student.route('/download_declaratie_firma', methods=["GET"])
def download_declaratie_firma():
    from service.utility import get_declaratie_firma_service

    service = get_declaratie_firma_service()
    doc = service.get_with_student_id(session["id"])
    content = doc.content

    return Response(content, mimetype="application/pdf", headers={"Content-disposition": "attachment; "
                                                                                         "filename=declaratie.pdf"})


@student.route('/download_declaratie_traseu', methods=["GET"])
def download_declaratie_traseu():
    from service.utility import get_declaratie_traseu_service

    service = get_declaratie_traseu_service()
    doc = service.getOne(session["id"])
    content = doc.content

    return Response(content, mimetype="application/pdf", headers={"Content-disposition": "attachment; "
                                                                                         "filename=declaratie.pdf"})


@student.route('/download', methods=["GET", "POST"])
def download():
    try:
        from service.utility import get_student_info_service, get_student_internship_service, get_internship_service,\
            get_tutor_info_service, get_student_activity_service
        import os

        id = session["id"]

        student_info_service = get_student_info_service()
        student_internship_service = get_student_internship_service()
        internship_service = get_internship_service()
        tutor_info_service = get_tutor_info_service()
        student_activity_service = get_student_activity_service()

        student_info = student_info_service.getOne(id)
        student_internship = student_internship_service.get_by_student_id(id)
        internship = internship_service.getOne(student_internship.internship_id)
        tutor = tutor_info_service.getOne(student_internship.tutor_id)
        activities = student_activity_service.get_all_with_student_id(id)

        from controller.form_utility import create_activity_html
        parameters = {}
        parameters["name"] = student_info.name
        parameters["faculty"] = student_info.faculty
        parameters["specialization"] = student_info.specialization
        parameters["year"] = str(student_info.year)
        parameters["tutor_name"] = tutor.name
        parameters["start_date"] = str(internship.start_date)
        parameters["end_date"] = str(internship.end_date)

        activity_list = []
        for activity in activities:
            activity_list.append((activity.period + "/" + activity.no_hours, activity.description))
        parameters["activities"] = activity_list
        create_activity_html(parameters, "Activity_" + student_info.name + ".html")

        import pdfkit
        import time

        pdfkit.from_file("Activity_" + student_info.name + ".html", "Activity_" + student_info.name + ".pdf")

        time.sleep(1)

        return send_from_directory(os.path.dirname(os.path.realpath(__file__)), "Activity_" + student_info.name + ".pdf")
    except ValueError as e:
        flash("Nu s-a putut genera raportul")
    return render_template("student/raportStudent.html")


# @auth_required_with_role(0)
@student.route('/student', methods=["GET"])
def home():
    if verify_role(0) == 0:
        return  redirect(url_for(get_home_route()))

    from service.utility import get_student_internship_service

    return render_template("student/homeStudent.html")
