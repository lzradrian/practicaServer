from typing import Any

from controller import db


class StudentInfo(db.Model):
    __tablename__ = 'StudentInfos'
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column("student_id", db.Integer, db.ForeignKey('Users.id'))
    name = db.Column("name", db.String)
    pnc = db.Column("pnc", db.String)  # CNP
    student_function = db.Column("student_function", db.String)  # licenta/master
    year = db.Column("year", db.Integer)
    group = db.Column("group", db.String)
    specialization = db.Column("specialization", db.String)
    study_line = db.Column("study_line", db.String)

    def __init__(self, id, student_id, name, pnc, student_function, year, group, specialization, study_line):
        self.id = id
        self.student_id = student_id
        self.name = name
        self.pnc = pnc
        self.student_function = student_function
        self.year = year
        self.group = group
        self.specialization = specialization
        self.study_line = study_line
