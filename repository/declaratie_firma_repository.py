class DeclaratieFirmaRepository:
    def getAll(self):
        from domain.declaratie_firma import DeclaratieFirma
        declaratii = DeclaratieFirma.query.all()
        return declaratii

    def getOne(self, id):
        from domain.declaratie_firma import DeclaratieFirma
        declaratie = DeclaratieFirma.query.get(id)
        return declaratie

    def get_with_student_id(self, student_id):
        from domain.declaratie_firma import DeclaratieFirma
        declaratie = DeclaratieFirma.query.filter_by(student_id=student_id).first()
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
        declaratie_found = self.get_with_student_id(declaratie.student_id)
        declaratie_found.submitted = declaratie.submitted
        declaratie_found.content = declaratie.content
        declaratie_found.checked = declaratie.checked
        db.session.commit()
        return declaratie
