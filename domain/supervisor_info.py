from typing import Any

from controller import db


class SupervisorInfo(db.Model):
    __tablename__ = 'SupervisorInfos'
    #Foreign key associated with column 'SupervisorInfos.id' could not find table 'Users'
    #id = db.Column("id", db.Integer, db.ForeignKey('Users.id'), primary_key=True)
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String)
    specialization = db.Column("specialization", db.String)
    email = db.Column("email", db.String)
    phone = db.Column("phone", db.String)
    fax = db.Column("fax", db.String)
    def __init__(self, id, name,specialization,email,phone,fax):
        self.id = id
        self.name = name
        self.email=email
        self.specialization=specialization
        self.phone=phone
        self.fax=fax

