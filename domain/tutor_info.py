from typing import Any

from controller import db
from domain.user import User  # rezolva problema cu foreign key


class TutorInfo(db.Model):
    __tablename__ = 'TutorInfos'
    id = db.Column("id", db.Integer, db.ForeignKey('Users.id'), primary_key=True)
    name = db.Column("name", db.String)
    email = db.Column("email", db.String)
    phone = db.Column("phone", db.String)
    fax = db.Column("fax", db.String)
    function = db.Column("function", db.String)

    def __init__(self, tutor_id, name, email, phone, fax, function):
        self.id = tutor_id
        self.name = name
        self.email = email
        self.phone = phone
        self.fax = fax
        self.function = function