from typing import Any

from controller import db


class SupervisorInfo(db.Model):
    __tablename__ = 'SupervisorInfos'
    id = db.Column("id", db.Integer, db.ForeignKey('Users.id'), primary_key=True)
    name = db.Column("name", db.String)
    function = db.Column("function", db.String)
    email = db.Column("email", db.String)
    phone = db.Column("phone", db.String)
    fax = db.Column("fax", db.String)
    def __init__(self, id, name,function,email,phone,fax):
        self.id = id
        self.name = name
        self.email=email
        self.function=function
        self.phone=phone
        self.fax=fax
