from controller import db


class StudentInternship(db.Model):
    __tablename__ = 'StudentInternships'
    internship_id = db.Column("internship_id", db.Integer, db.ForeignKey('Internships.id'), primary_key=True)
    student_id = db.Column("student_id", db.Integer, db.ForeignKey('Users.id'))
    tutor_id = db.Column("tutor_id", db.Integer, db.ForeignKey('Users.id'))
    supervisor_id = db.Column("supervisor_id", db.Integer, db.ForeignKey('Users.id'))

    def __init__(self, internship_id, student_id, tutor_id, supervisor_id):
        self.id = id
        self.internship_id = internship_id
        self.student_id = student_id
        self.tutor_id = tutor_id
        self.supervisor_id = supervisor_id
