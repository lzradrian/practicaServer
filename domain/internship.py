from controller import db

class Internship(db.Model):
    __tablename__ = 'Internships'
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    representative_id = db.Column("representative_id", db.Integer, db.ForeignKey('Users.id'))
    year = db.Column("year", db.Integer)
    start_date = db.Column("start_date", db.Date)
    end_date = db.Column("end_date", db.Date)
    awards = db.Column("awards", db.String)
    rewards= db.Column("rewards", db.String)
    otherConditions= db.Column("otherConditions", db.String)
    workContract = db.Column("workContract", db.String)
    noWorkContract= db.Column("noWorkContract", db.String)
    EUFinanced= db.Column("EUFinanced", db.String)
    projectBased= db.Column("projectBased", db.String)
    projectName= db.Column("projectName", db.String)
    hours= db.Column("hours", db.String)
    def __init__(self, id, representative_id, year, start_date, end_date):
        self.id = id
        self.representative_id = representative_id
        self.year = year
        self.start_date = start_date
        self.end_date = end_date

    def __init__(self, id, representative_id, year, start_date, end_date,awards,rewards,otherConditions
                 ,workContract,noWorkContract,EUFinanced, projectBased,projectName,hours):
        self.id = id
        self.representative_id = representative_id
        self.year = year
        self.start_date = start_date
        self.end_date = end_date
        self.awards=awards
        self.rewards=rewards
        self.otherConditions=otherConditions
        self.workContract=workContract
        self.noWorkContract=noWorkContract
        self.EUFinanced=EUFinanced
        self.projectName=projectName
        self.projectBased=projectBased
        self.hours=hours
