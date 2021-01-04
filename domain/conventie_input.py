from controller import db

fields = [(), ]

class ConventieInput(db.Model):
    __tablename__ = 'ConventieInput'
    _id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    content = db.Column("content", db.String)
    completedByStudent = db.Column("completedByStudent", db.BOOLEAN)
    completedByFirmaResponsabil = db.Column("completedByFirmaResponsabil", db.BOOLEAN)
    completedByFirmaTutori = db.Column("completedByFirmaTutori", db.BOOLEAN)
    completedByCadruDidacticSupervizor = db.Column("completedByCadruDidacticSupervizor", db.BOOLEAN)
    completedByDecan = db.Column("completedByDecan", db.BOOLEAN)

    def __init__(self, content):
        self.content = content
        self.completedByStudent = False
        self.completedByFirmaResponsabil = False
        self.completedByFirmaTutori = False
        self.completedByCadruDidacticSupervizor = False
        self.completedByDecan = False

    def set_id(self, value):
        self._id = value

    def set_content(self, value):
        self.content = value

    def set_completedByStudent(self, value):
        self.completedByStudent = value

    def set_completedByFirmaResponsabil(self, value):
        self.completedByFirmaResponsabil = value

    def set_completedByFirmaTutori(self, value):
        self.completedByFirmaTutori = value

    def set_completedByCadruDidacticSupervizor(self, value):
        self.completedByCadruDidacticSupervizor = value

    def set_completedByDecan(self, value):
        self.completedByDecan = value

    def get_id(self):
        return self._id

    def get_content(self):
        return self.content

    def get_completedByStudent(self):
        return self.completedByStudent

    def get_completedByFirmaResponsabil(self):
        return self.completedByFirmaResponsabil

    def get_completedByFirmaTutori(self):
        return self.completedByFirmaTutori

    def get_completedByCadruDidacticSupervizor(self):
        return self.completedByCadruDidacticSupervizor

    def get_completedByDecan(self):
        return self.completedByDecan
