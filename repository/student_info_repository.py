class StudentInfoRepository:
    def getAll(self):
        from domain.student_info import StudentInfo
        infos = StudentInfo.query.all()
        return infos

    def getOne(self, id):
        from domain.student_info import StudentInfo
        student_info = StudentInfo.query.get(id)
        return student_info

    '''
    def get_by_student_id(self, student_id):
        from domain.student_info import StudentInfo
        student_info = StudentInfo.query.filter_by(student_id=student_id).first()
        return student_info
    '''

    def get_by_identifiers(self, name, year, group):
        from domain.student_info import StudentInfo
        student_info = StudentInfo.query.filter_by(name=name).filter_by(year=int(year)).filter_by(group=group).first()
        return student_info

    def add(self, student_info):
        from controller import db
        db.session.add(student_info)
        db.session.commit()
        return student_info

    def remove(self, student_info):
        from controller import db
        db.session.delete(student_info)
        db.session.commit()

    def update(self, student_info):
        from controller import db
        from domain.student_info import StudentInfo
        student_info_found = StudentInfo.query.get(student_info.get_id())
        student_info_found.name = student_info.name
        student_info_found.pnc = student_info.pnc
        student_info_found.student_function = student_info.student_function
        student_info_found.year = student_info.year
        student_info_found.group = student_info.group
        student_info_found.specialization = student_info.specialization
        student_info_found.study_line = student_info.study_line
        db.session.commit()
        return student_info

