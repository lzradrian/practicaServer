from database.database_config import Config
from flask_sqlalchemy import SQLAlchemy
from domain.conventie_input import ConventieInput
from domain.user import User
from domain.acordPractica import AcordPractica
from domain.company_info import CompanyInfo
from domain.conventie_input import ConventieInput
from domain.student_info import StudentInfo


def run():
    from controller import db
    db.create_all()


run()
