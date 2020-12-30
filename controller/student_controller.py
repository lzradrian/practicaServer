from flask import Blueprint, redirect, flash, render_template, session, request, url_for

from controller.helpers.authorize import verify_role, auth_required_with_role
from repository.conventie_repository import ConventieRepository
from service.conventie_service import ConventieService

student = Blueprint('student', __name__)


def create_conventie_input_txt(name, country, city, street, number, apartment, county, phone, email, cnp, series, id,
                               birthdate, birthcity, birthcounty, function, year, group, specialty, lineOfStudy, date,
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
        line = line.replace("StudentYear Year", "StudentYear " + year)
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
    conventieService.add(conventie)


@student.route("/student_conventie", methods=["POST", "GET"])
def conventie():
    if request.method == "POST":

        name = request.form["name"]
        country = request.form["country"]
        city = request.form["city"]
        street = request.form["street"]
        number = request.form["number"]
        apartment = request.form["apartment"]
        county = request.form["county"]
        phone = request.form["phone"]
        email = request.form["email"]
        cnp = request.form["cnp"]
        series = request.form["series"]
        id = request.form["id"]
        birthdate = request.form["birthdate"]
        birthcity = request.form["birthcity"]
        birthcounty = request.form["birthcounty"]
        function = request.form["function"]
        year = request.form["year"]
        group = request.form["group"]
        specialty = request.form["specialty"]
        line = request.form["line"]
        date = request.form["date"]
        signature = request.form["signature"]

        create_conventie_input_txt(name, country, city, street, number, apartment, county, phone, email, cnp, series,
                                   id, birthdate, birthcity, birthcounty, function, year, group, specialty, line, date,
                                   signature)

        return render_template("student/conventieStudent.html")
    else:
        return render_template("student/conventieStudent.html")


# @auth_required_with_role(0)
@student.route('/student', methods=["GET"])
def home():
    if verify_role(0) == 0:
        return render_template("home.html")
    return render_template("student/homeStudent.html")
