from controller import db


class DeclaratieUBB(db.Model):
    __tablename__ = 'DeclaratieUBB'
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column("student_id", db.Integer, db.ForeignKey('Users.id'))
    submitted = db.Column("submitted", db.DateTime)
    content = db.Column("content", db.PickleType)
    checked = db.Column("checked", db.Boolean)

    def __init__(self, id, student_id, submitted, content, checked):
        self.id = id
        self.student_id = student_id
        self.submitted = submitted
        self.content = content
        self.checked = checked
