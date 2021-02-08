class InternshipRepository:
    def get_all(self):
        from domain.internship import Internship
        internships = Internship.query.all()
        return internships

    def get_one(self, id):
        from domain.internship import Internship
        internship = Internship.query.get(id)
        return internship

    def get_by_representative_id(self, representative_id):
        from domain.internship import Internship
        internship = Internship.query.filter_by(representative_id=representative_id).first()
        return internship

    def add(self, internship):
        from controller import db
        db.session.add(internship)
        db.session.commit()
        return internship

    def remove(self, internship):
        from controller import db
        db.session.delete(internship)
        db.session.commit()

    def update(self, internship):
        from controller import db
        from domain.internship import Internship
        internship_found = Internship.query.get(internship.id)
        # todo
        return internship
