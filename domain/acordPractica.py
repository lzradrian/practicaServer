from controller import db


class AcordPractica(db.Model):
    __tablename__ = 'AcordPractica'
    _id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    content = db.Column("content", db.String)
    completedByFirmaReprezentant = db.Column("completedByFirmaReprezentant", db.BOOLEAN)
    completedByDepJuridicUBB = db.Column("completedByDepJuridicUBB", db.BOOLEAN)

    def __init__(self, content):
        self.content = content
        self.completedByFirmaReprezentant = False
        self.completedByDepJuridicUBB = False

    def set_id(self, value):
        self._id = value

    def set_content(self, value):
        self.content = value

    def set_completedByFirmaReprezentant(self, value):
        self.completedByFirmaReprezentant = value

    def set_completedByDepJuridicUBB(self, value):
        self.completedByFirmaReprezentant = value

    def get_id(self):
        return self._id

    def get_content(self):
        return self.content

    def get_completedByFirmaReprezentant(self):
        return self.completedByFirmaReprezentant

    def get_completedByDepJuridicUBB(self):
        return self.completedByFirmaReprezentant
