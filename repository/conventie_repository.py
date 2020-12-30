class ConventieRepository:

    def getAll(self):
        from domain.conventie_input import ConventieInput
        conventii = ConventieInput.query.all()
        return conventii

    def getOne(self,id):
        from domain.conventie_input import ConventieInput
        conventie =ConventieInput.query.get(id)
        return conventie

    def add(self,conventie):
        from controller import db
        db.session.add(conventie)
        db.session.commit()
        return conventie

    def remove(self,conventie):
        from controller import db
        db.session.delete(conventie)
        db.session.commit()

    def update(self,conventie):
        from controller import db
        from domain.conventie_input import ConventieInput
        conventiefound = ConventieInput.query.get(conventie.get_id())
        conventiefound.set_content(conventie.get_content())
        conventiefound.set_completedByStudent(conventie.get_completedByStudent())
        conventiefound.set_completedByFirmaResponsabil(conventie.get_completedByFirmaResponsabil())
        conventiefound.set_completedByFirmaTutori(conventie.get_completedByFirmaTutori())
        conventiefound.set_completedByCadruDidacticSupervizor(conventie.get_completedByCadruDidacticSupervizor())
        conventiefound.set_completedByDecan(conventie.get_completedByDecan())
        db.session.commit()
        return conventie
