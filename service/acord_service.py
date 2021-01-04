class AcordService:
    def __init__(self, __repo):
        self.__repo = __repo

    def add(self, acord):
        acordfound = self.__repo.getOne(acord.get_id())
        if (acordfound != None):
            raise ValueError("Already exists a acord with given id")
        return self.__repo.add(acord)

    def getAll(self):
        acord = self.__repo.getAll()
        return acord

    def getOne(self, id):
        acord = self.__repo.getOne(id)
        if (acord == None):
            raise ValueError("acord with given id does not exist.")
        return acord

    def remove(self, id):
        acord = self.__repo.getOne(id)
        if (acord == None):
            raise ValueError("acord with given id does not exist.")
        self.__repo.remove(acord)

    def update(self, acord):
        acordfound = self.__repo.getOne(acord.get_id())
        if (acordfound == None):
            raise ValueError("acord with given id does not exist.")
        self.__repo.update(acord)
        return acord
