class TutorInfoRepository:
    def getAll(self):
        from domain.tutor_info import TutorInfo
        infos = TutorInfo.query.all()
        return infos

    def getOne(self, id):
        from domain.tutor_info import TutorInfo
        tutor_info = TutorInfo.query.get(id)
        return tutor_info

    def get_by_name(self, name):
        from domain.tutor_info import TutorInfo
        tutor_info = TutorInfo.query.filter_by(name=name).first()
        return tutor_info

    def add(self, tutor_info):
        from controller import db
        db.session.add(tutor_info)
        db.session.commit()
        return tutor_info

    def remove(self, tutor_info):
        from controller import db
        db.session.delete(tutor_info)
        db.session.commit()

    def update(self, tutor_info):
        from controller import db
        from domain.tutor_info import TutorInfo
        db.session.commit()
        return tutor_info

