from controller import db


class StudentInternship(db.Model):
    __tablename__ = 'StudentInternships'
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    internship_id = db.Column("internship_id", db.Integer, db.ForeignKey('Internships.id'))
    student_id = db.Column("student_id", db.Integer, db.ForeignKey('Users.id'))
    tutor_id = db.Column("tutor_id", db.Integer, db.ForeignKey('Users.id'))

    def __init__(self, id, internship_id, student_id, tutor_id):
        self.id = id
        self.internship_id = internship_id
        self.student_id = student_id
        self.tutor_id = tutor_id
