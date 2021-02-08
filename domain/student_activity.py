from controller import db


class StudentActivity(db.Model):
    __tablename__ = 'StudentActivities'
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column("student_id", db.Integer)
    period = db.Column("period", db.String)
    no_hours = db.Column("no_hours", db.Integer)
    description = db.Column("description", db.Integer)

    def __init__(self, id, student_id, period, no_hours, description):
        self.id = id
        self.student_id = student_id
        self.period = period
        self.no_hours = no_hours
        self.description = description


