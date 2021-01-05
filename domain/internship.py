from controller import db

class Internship(db.Model):
    __tablename__ = 'Internships'
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    representative_id = db.Column("representative_id", db.Integer, db.ForeignKey('Users.id'))
    year = db.Column("year", db.Integer)
    start_date = db.Column("start_date", db.Date)
    end_date = db.Column("end_date", db.Date)

    def __init__(self, id, representative_id, year, start_date, end_date):
        self.id = id
        self.representative_id = representative_id
        self.year = year
        self.start_date = start_date
        self.end_date = end_date

