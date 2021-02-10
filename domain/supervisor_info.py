from typing import Any

from controller import db


class SupervisorInfo(db.Model):
    __tablename__ = 'SupervisorInfos'
    id = db.Column("id", db.Integer, db.ForeignKey('Users.id'), primary_key=True)
    name = db.Column("name", db.String)
    specialization = db.Column("specialization", db.String)

    def __init__(self, id, name, specialization):
        self.id = id
        self.name = name
        self.specialization = specialization
