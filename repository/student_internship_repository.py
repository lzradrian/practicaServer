class StudentInternshipRepository:
    def get_all(self):
        from domain.student_internship import StudentInternship
        student_internships = StudentInternship.query.all()
        return student_internships

    def get_one(self, id):
        from domain.student_internship import StudentInternship
        student_internship = StudentInternship.query.filter_by(student_id=id).first()
        return student_internship

    def get_by_internship_id(self, internship_id):
        from domain.student_internship import StudentInternship
        student_internship = StudentInternship.query.filter_by(internship_id=internship_id).all()
        return student_internship

    def get_by_student_id(self, student_id):
        from domain.student_internship import StudentInternship
        student_internship = StudentInternship.query.filter_by(student_id=student_id).first()
        return student_internship

    def add(self, student_internship):
        from controller import db
        db.session.add(student_internship)
        db.session.commit()
        return student_internship

    def remove(self, student_internship):
        from controller import db
        db.session.delete(student_internship)
        db.session.commit()

    def update(self, student_internship):
        from controller import db
        from domain.student_internship import StudentInternship
        student_internship_found = student_internship.query.get(student_internship.id)
        # todo
        return student_internship
