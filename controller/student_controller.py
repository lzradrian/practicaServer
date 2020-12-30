from flask import Blueprint, redirect, flash, render_template, session, request, url_for

from controller.helpers.authorize import verify_role, auth_required_with_role
from repository.conventie_repository import ConventieRepository
from service.conventie_service import ConventieService

student = Blueprint('student', __name__)


def create_conventie_input_txt(nume):
    import os
    dir_location = os.getcwd()
    while dir_location[-1] != "\\":
        dir_location = dir_location[:-1]
    dir_location_input = dir_location[:-1] + "\\forms\\conventie_input.txt"
    #dir_location_output = dir_location[:-1] + "\\forms\\test_output.txt"

    file = open(dir_location_input, "r")
    replaced_content = ""
    for line in file:
        line = line.strip()
        #todo: line.replace si pentru alte date
        line = line.replace("StudentName Name", "StudentName " + nume)
        line = line.replace("StudentCity City", "StudentCity " + nume)
        line = line.replace("StudentStreet Street", "StudentStreet " + nume)
        line = line.replace("StudentPNC 123456789", "StudentPNC " + nume)
        line = line.replace("StudentDateOfBirth 1990.10.10", "StudentDateOfBirth " + nume)
        line = line.replace("StudentPhone 123456789", "StudentPhone " + nume)
        line = line.replace("StudentCounty County", "StudentCounty " + nume)
        line = line.replace("StudentApartment 10", "StudentApartment " + nume)
        line = line.replace("StudentStudyLine Line", "StudentStudyLine " + nume)
        line = line.replace("StudentBirthLocation Location", "StudentBirthLocation " + nume)
        line = line.replace("StudentSpecialization Spec", "StudentSpecialization " + nume)
        line = line.replace("StudentNationality Nationality", "StudentNationality " + nume)
        line = line.replace("StudentGroup Group", "StudentGroup " + nume)
        line = line.replace("StudentYear Year", "StudentYear " + nume)
        line = line.replace("StudentICSeries 123", "StudentICSeries " + nume)
        line = line.replace("StudentStreetNo 123", "StudentStreetNo " + nume)
        line = line.replace("StudentICNo 123", "StudentICNo " + nume)
        line = line.replace("StudentNationality Nationality", "StudentNationality " + nume)
        line = line.replace("SignStudentName Name", "SignStudentName " + nume)
        line = line.replace("SignStudentDate Date", "SignStudentDate " + nume)
        replaced_content = replaced_content + line + "\n"
    file.close()

    from domain.conventie_input import ConventieInput
    conventieRepo = ConventieRepository()
    conventieService = ConventieService(conventieRepo)
    conventie = ConventieInput(replaced_content)
    conventie.set_completedByStudent(True)
    conventieService.add(conventie)


# @auth_required_with_role(0)
@student.route('/student', methods=["POST", "GET"])
def home():
    if request.method == "POST":

        numeStudent = "numeStudent"
        #todo:obtinerea tuturor datelor din formular

        create_conventie_input_txt(numeStudent)

        return render_template("homeStudent.html")
    else:
        if verify_role(0) == 0:
            return render_template("home.html")
        return render_template("homeStudent.html")
