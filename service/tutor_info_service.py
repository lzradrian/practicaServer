class TutorInfoService:
    def __init__(self, __repo):
        self.__repo = __repo

    def add(self, tutor_info):
        tutor_info_found = self.__repo.getOne(tutor_info.id)
        if tutor_info_found is not None:
            raise ValueError("Already exists a TutorInfo with given id")
        return self.__repo.add(tutor_info)

    def getAll(self):
        tutor_infos = self.__repo.getAll()
        return tutor_infos

    def getOne(self, id):
        tutor_info = self.__repo.getOne(id)
        if tutor_info is None:
            raise ValueError("TutorInfo with given id does not exist.")
        return tutor_info

    def get_by_identifiers(self, name, year, group):
        tutor_info = self.__repo.get_by_identifiers(name, year, group)
        if tutor_info is None:
            raise ValueError("TutorInfo with given tutor_id does not exist.")
        return tutor_info

    def remove(self, id):
        tutor_info = self.__repo.getOne(id)
        if tutor_info is None:
            raise ValueError("TutorInfo with given id does not exist.")
        self.__repo.remove(tutor_info)

    def update(self, tutor_info):
        tutor_info_found = self.__repo.getOne(tutor_info.get_id())
        if tutor_info_found is None:
            raise ValueError("TutorInfo with given id does not exist.")
        self.__repo.update(tutor_info)
        return tutor_info
