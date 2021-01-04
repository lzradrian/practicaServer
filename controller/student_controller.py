from flask import Blueprint, redirect, flash, render_template, session, request, url_for

from controller.helpers.authorize import verify_role, auth_required_with_role
from controller.helpers.pdfTools import create_pdf_from_dic
from repository.conventie_repository import ConventieRepository
from service.conventie_service import ConventieService

student = Blueprint('student', __name__)

def create_conventie_input(name, country, city, street, number, apartment, county, phone, email, cnp, series, id,
                           birthdate, birthcity, function, year, group, specialty, lineOfStudy, date,
                           signature):
    import os
    dir_location = os.getcwd()
    while dir_location[-1] != "\\":
        dir_location = dir_location[:-1]
    dir_location_input = dir_location[:-1] + "\\forms\\conventie_input.txt"

    file = open(dir_location_input, "r")
    replaced_content = ""
    for line in file:
        line = line.strip()
        # todo: rezolvarea diferentelor dintre input-ul din form si pdf (ex: signature etc)
        line = line.replace("StudentName Name", "StudentName " + name)
        line = line.replace("StudentCity City", "StudentCity " + city)
        line = line.replace("StudentStreet Street", "StudentStreet " + street)
        line = line.replace("StudentPNC 123456789", "StudentPNC " + cnp)
        line = line.replace("StudentDateOfBirth 1990.10.10", "StudentDateOfBirth " + birthdate)
        line = line.replace("StudentPhone 123456789", "StudentPhone " + phone)
        line = line.replace("StudentEmail Email", "StudentEmail " + email)
        line = line.replace("StudentCounty County", "StudentCounty " + county)
        line = line.replace("StudentApartment 10", "StudentApartment " + apartment)
        line = line.replace("StudentStudyLine Line", "StudentStudyLine " + lineOfStudy)
        line = line.replace("StudentRole Student", "StudentRole " + function)
        line = line.replace("StudentBirthLocation Location", "StudentBirthLocation " + birthcity)
        line = line.replace("StudentSpecialization Spec", "StudentSpecialization " + specialty)
        line = line.replace("StudentNationality Nationality", "StudentNationality " + country)
        line = line.replace("StudentGroup Group", "StudentGroup " + group)
        line = line.replace("StudentYear Year", "StudentYear " + str(year))
        line = line.replace("StudentICSeries 123", "StudentICSeries " + series)
        line = line.replace("StudentStreetNo 123", "StudentStreetNo " + number)
        line = line.replace("StudentICNo 123", "StudentICNo " + id)
        line = line.replace("StudentNationality Nationality", "StudentNationality " + country)
        line = line.replace("SignStudentName Name", "SignStudentName " + name)
        line = line.replace("SignStudentDate Date", "SignStudentDate " + date)

        replaced_content = replaced_content + line + "\n"
    file.close()

    from domain.conventie_input import ConventieInput
    conventieRepo = ConventieRepository()
    conventieService = ConventieService(conventieRepo)
    conventie = ConventieInput(replaced_content)
    conventie.set_completedByStudent(True)
    conventieService.add_or_update(conventie)


@student.route("/student_conventie", methods=["POST", "GET"])
def conventie():
    if request.method == "POST":
        from repository.student_info_repository import StudentInfoRepository
        from service.student_info_service import StudentInfoService
        from domain.student_info import StudentInfo
        from domain.conventie_student_file import fields
        repo = StudentInfoRepository()
        service = StudentInfoService(repo)

        info = service.getOne(session["id"])

        name = info.name
        cnp = info.pnc
        group = info.group
        specialty = info.specialization
        year = info.year
        function = info.student_function
        line = info.study_line

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
        date = request.form["signdate"]
        signature = request.form["signature"] #nefolosit ulterior

        '''
        #varianta2
        #params = [info.name, info.pnc, info.group, info.specialization, info.year,
        #          info.study_line,request.form["city"], request.form["street"],
        #          request.form["number"],request.form["apartment"], request.form["county"] ,request.form["phone"],
        #          request.form["email"],request.form["series"],request.form["id"], request.form["birthdate"],
        #          request.form["birthlocation"] ,info.student_function,request.form["nationality"] ,request.form["signdate"]
        #         ,info.name
        #          ]
        #pair_input = dict(zip(fields.keys(), params))

        #content=""
        #for k, v in pair_input.items():
        #    content= content+ str(k) + " "+ str(v) + "\n"

        #from domain.conventie_input import ConventieInput
        #conventieRepo = ConventieRepository()
        #conventieService = ConventieService(conventieRepo)
        #conventie = ConventieInput(content)
        #conventie.set_completedByStudent(True)
        #conventieService.add_or_update(conventie)

        #create_pdf_from_dic("ConventiePractica.pdf", "outputConventie.pdf", pair_input)
        '''
        create_conventie_input(name, country, city, street, number, apartment, county, phone, email, cnp, series,
                               id, birthdate, birthcity, function, year, group, specialty, line, date,
                               signature)

        return redirect(url_for("student.home"))
    else:
        return render_template("student/conventieStudent.html")


@student.route("/student_company_declaration", methods=["POST", "GET"])
def student_company_declaration():
    if request.method == "POST":
        from repository.student_info_repository import StudentInfoRepository
        from service.student_info_service import StudentInfoService
        from domain.student_info import StudentInfo
        from datetime import date
        from domain.declaratie_firma_file import fields
        from controller.form_utility import write_to_file, generate_pdf
        from controller.helpers.pdfTools import create_pdf_from_dic

        repo = StudentInfoRepository()
        service = StudentInfoService(repo)

        info = service.getOne(session["id"])

        date = str(date.today())
        params = [info.name, info.group, info.specialization, info.year,
                  request.form["interval"], date, request.form["address"],
                  request.form["firm"], request.form["coordinator"]]
        pair_input = dict(zip(fields.keys(), params))
        create_pdf_from_dic("DeclaratieActivitateFirma.pdf", "outputFirma.pdf", pair_input)
        '''
        write_to_file("company_declaration_input.txt", pair_input)
        generate_pdf("../forms/DeclaratieActivitateFirma.pdf",
                     "DeclaratieActivitateFirma-" + info.name,
                     "company_declaration_input.txt")
        '''
        return redirect(url_for("student.home"))
    return render_template("student/declaratieFirmaStudent.html")


@student.route("/student_uni_declaration", methods=["POST", "GET"])
def student_uni_declaration():
    if request.method == "POST":
        from repository.student_info_repository import StudentInfoRepository
        from service.student_info_service import StudentInfoService
        from domain.student_info import StudentInfo
        from datetime import date
        from domain.declaratie_ubb_file import fields
        from controller.form_utility import write_to_file, generate_pdf
        from controller.helpers.pdfTools import create_pdf_from_dic

        repo = StudentInfoRepository()
        service = StudentInfoService(repo)

        info = service.getOne(session["id"])
        date = str(date.today())
        params = [info.name, info.group, info.specialization, info.year,
                  request.form["interval"], date, request.form["address"],
                  request.form["coordinator"]]
        pair_input = dict(zip(fields.keys(), params))
        create_pdf_from_dic("DeclaratieActivitateUBB.pdf","outputUBB.pdf",pair_input)
        '''
                write_to_file("company_declaration_input.txt", pair_input)
                generate_pdf("../forms/DeclaratieActivitateFirma.pdf",
                             "DeclaratieActivitateFirma-" + info.name,
                             "company_declaration_input.txt")
        '''
        return redirect(url_for("student.home"))
    return render_template("student/declaratieFacultateStudent.html")


@student.route("/student_info", methods=["POST", "GET"])
def student_info():
    if request.method == "POST":
        student_id = session["id"]
        name = request.form["name"]
        pnc = request.form["pnc"]
        student_function = request.form["student_function"]
        year = request.form["year"]
        group = request.form["group"]
        specialization = request.form["specialization"]
        study_line = request.form["specialization"]

        from repository.student_info_repository import StudentInfoRepository
        from service.student_info_service import StudentInfoService
        from domain.student_info import StudentInfo

        repo = StudentInfoRepository()
        service = StudentInfoService(repo)
        studentinfo = StudentInfo(student_id, name, pnc, student_function,
                               year, group, specialization, study_line)
        try:
            service.add(studentinfo)
            flash("Ati completat cu succes datele!")
        except ValueError:
            service.update(studentinfo)
            flash("Ati updatat cu succes datele!")
        return redirect(url_for("student.home"))
    else:
        return render_template("student/infoStudent.html")


# @auth_required_with_role(0)
@student.route('/student', methods=["GET"])
def home():
    if verify_role(0) == 0:
        return render_template("home.html")
    return render_template("student/homeStudent.html")
