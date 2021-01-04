class AcordRepository:

    def getAll(self):
        from domain.acordPractica import AcordPractica
        acord = AcordPractica.query.all()
        return acord

    def getOne(self, id):
        from domain.acordPractica import AcordPractica
        acord = AcordPractica.query.get(id)
        return acord

    def add(self, acord):
        from controller import db
        db.session.add(acord)
        db.session.commit()
        return acord

    def remove(self, acord):
        from controller import db
        db.session.delete(acord)
        db.session.commit()

    def update(self, acord):
        from controller import db
        from domain.acordPractica import AcordPractica
        acordfound = AcordPractica.query.get(acord.get_id())
        acordfound.set_content(acord.get_content())
        acordfound.set_completedByDepJuridicUBB(acord.get_completedByDepJuridicUBB())
        acordfound.set_completedByFirmaReprezentant(acord.get_completedByFirmaReprezentant())
        db.session.commit()
        return acord
