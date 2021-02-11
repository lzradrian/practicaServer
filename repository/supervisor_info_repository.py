class SupervisorInfoRepository:
    def getAll(self):
        from domain.supervisor_info import SupervisorInfo
        infos = SupervisorInfo.query.all()
        return infos

    def getOne(self, id):
        from domain.supervisor_info import SupervisorInfo
        supervisor_info = SupervisorInfo.query.get(id)
        return supervisor_info

    def get_by_name(self, name):
        from domain.supervisor_info import SupervisorInfo
        supervisor_info = SupervisorInfo.query.filter_by(name=name).first()
        return supervisor_info

    def add(self, supervisor_info):
        from controller import db
        db.session.add(supervisor_info)
        db.session.commit()
        return supervisor_info

    def remove(self, supervisor_info):
        from controller import db
        db.session.delete(supervisor_info)
        db.session.commit()

    def update(self, supervisor_info):
        from controller import db
        from domain.supervisor_info import SupervisorInfo
        supervisor_info_found = SupervisorInfo.query.get(supervisor_info.id)
        supervisor_info_found.name = supervisor_info.name
        supervisor_info_found.specialization=supervisor_info.specialization
        supervisor_info_found.phone=supervisor_info.phone
        supervisor_info_found.fax=supervisor_info.fax
        db.session.commit()
        return supervisor_info

