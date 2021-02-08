class SupervisorInfoService:
    def __init__(self, __repo):
        self.__repo = __repo

    def add(self, supervisor_info):
        supervisor_info_found = self.__repo.getOne(supervisor_info.id)
        if supervisor_info_found is not None:
            raise ValueError("Already exists a SupervisorInfo with given id")
        return self.__repo.add(supervisor_info)

    def getAll(self):
        supervisor_infos = self.__repo.getAll()
        return supervisor_infos

    def getOne(self, id):
        supervisor_info = self.__repo.getOne(id)
        if supervisor_info is None:
            raise ValueError("SupervisorInfo with given id does not exist.")
        return supervisor_info

    def get_by_name(self, name):
        supervisor_info = self.__repo.get_by_name(name)
        if supervisor_info is None:
            raise ValueError("SupervisorInfo with given student_id does not exist.")
        return supervisor_info

    def remove(self, id):
        supervisor_info = self.__repo.getOne(id)
        if supervisor_info is None:
            raise ValueError("SupervisorInfo with given id does not exist.")
        self.__repo.remove(supervisor_info)

    def update(self, supervisor_info):
        supervisor_info_found = self.__repo.getOne(supervisor_info.id)
        if supervisor_info_found is None:
            raise ValueError("SupervisorInfo with given id does not exist.")
        self.__repo.update(supervisor_info)
        return supervisor_info
