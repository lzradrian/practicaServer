from typing import Any

from controller import db
from domain.user import User  # rezolva problema cu foreign key


class StudentInfo(db.Model):
    __tablename__ = 'StudentInfos'
    id = db.Column("id", db.Integer, db.ForeignKey('Users.id'), primary_key=True)
    name = db.Column("name", db.String)
    pnc = db.Column("pnc", db.String)  # CNP
    student_function = db.Column("student_function", db.String)  # licenta/master
    faculty = db.Column("faculty", db.String)
    year = db.Column("year", db.Integer)
    group = db.Column("group", db.String)
    specialization = db.Column("specialization", db.String)
    study_line = db.Column("study_line", db.String)

    def __init__(self, student_id, name, pnc, student_function, faculty, year, group, specialization, study_line):
        self.id = student_id
        self.name = name
        self.pnc = pnc
        self.student_function = student_function
        self.faculty = faculty
        self.year = year
        self.group = group
        self.specialization = specialization
        self.study_line = study_line

    def get_id(self):
        return self.id
