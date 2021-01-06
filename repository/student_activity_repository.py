class StudentActivityRepository:
    def get_all(self):
        from domain.student_activity import StudentActivity
        student_activitys = StudentActivity.query.all()
        return student_activitys

    def get_one(self, id):
        from domain.student_activity import StudentActivity
        student_activity = StudentActivity.query.get(id)
        return student_activity

    def get_all_with_student_id(self, student_id):
        from domain.student_activity import StudentActivity
        student_activity = StudentActivity.query.filter_by(student_id=student_id).all()
        return student_activity

    def add(self, student_activity):
        from controller import db
        db.session.add(student_activity)
        db.session.commit()
        return student_activity

    def remove(self, student_activity):
        from controller import db
        db.session.delete(student_activity)
        db.session.commit()

    def update(self, student_activity):
        from controller import db
        from domain.student_activity import StudentActivity
        student_activity_found = StudentActivity.query.get(student_activity.id)
        # todo
        return student_activity
