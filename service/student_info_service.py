class StudentInfoService:
    def __init__(self, __repo):
        self.__repo = __repo

    def add(self, student_info):
        student_info_found = self.__repo.getOne(student_info.get_id())
        if student_info_found is not None:
            raise ValueError("Already exists a StudentInfo with given id")
        return self.__repo.add(student_info)

    def getAll(self):
        student_infos = self.__repo.getAll()
        return student_infos

    def getOne(self, id):
        student_info = self.__repo.getOne(id)
        if student_info is None:
            raise ValueError("StudentInfo with given id does not exist.")
        return student_info


    def get_by_identifiers(self, name, year, group):
        student_info = self.__repo.get_by_identifiers(name, year, group)
        if student_info is None:
            raise ValueError("StudentInfo with given student_id does not exist.")
        return student_info

    def remove(self, id):
        student_info = self.__repo.getOne(id)
        if student_info is None:
            raise ValueError("StudentInfo with given id does not exist.")
        self.__repo.remove(student_info)

    def update(self, student_info):
        student_info_found = self.__repo.getOne(student_info.get_id())
        if student_info_found is None:
            raise ValueError("StudentInfo with given id does not exist.")
        self.__repo.update(student_info)
        return student_info
