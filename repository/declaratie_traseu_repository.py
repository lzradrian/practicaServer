class DeclaratieTraseuRepository:
    def getAll(self):
        from domain.declaratie_traseu import DeclaratieTraseu
        declaratii = DeclaratieTraseu.query.all()
        return declaratii

    def getOne(self, id):
        from domain.declaratie_traseu import DeclaratieTraseu
        declaratie = DeclaratieTraseu.query.get(id)
        return declaratie


    def add(self, declaratie):
        from controller import db
        db.session.add(declaratie)
        db.session.commit()
        return declaratie

    def remove(self, declaratie):
        from controller import db
        db.session.delete(declaratie)
        db.session.commit()

    def update(self, declaratie):
        from controller import db
        declaratie_found = self.getOne(declaratie.student_id)
        declaratie_found.submitted = declaratie.submitted
        declaratie_found.content = declaratie.content
        declaratie_found.checked = declaratie.checked
        db.session.commit()
        return declaratie
