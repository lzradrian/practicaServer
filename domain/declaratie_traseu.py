from controller import db

class DeclaratieTraseu(db.Model):
    __tablename__ = 'DeclaratieTraseu'
    student_id = db.Column("student_id", db.Integer, db.ForeignKey('Users.id'), primary_key=True)
    submitted = db.Column("submitted", db.DateTime)
    content = db.Column("content", db.PickleType)
    checked = db.Column("checked", db.Boolean)

    def __init__(self, student_id, submitted, content, checked):
        self.student_id = student_id
        self.submitted = submitted
        self.content = content
        self.checked = checked
