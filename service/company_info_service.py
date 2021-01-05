class CompanyInfoService:
    def __init__(self, __repo):
        self.__repo = __repo

    def add(self, c):
        found = self.__repo.getOne(c.get_id())
        if (found != None):
            raise ValueError("Already exists a CompanyInfo with given id")
        return self.__repo.add(c)

    def getAll(self):
        c = self.__repo.getAll()
        return c

    def getOne(self, id):
        c = self.__repo.getOne(id)
        if (c == None):
            raise ValueError("CompanyInfo with given id does not exist.")
        return c

    def remove(self, id):
        c = self.__repo.getOne(id)
        if (c == None):
            raise ValueError("CompanyInfo with given id does not exist.")
        self.__repo.remove(c)

    def update(self, c):
        found = self.__repo.getOne(c.get_id())
        if (found == None):
            raise ValueError("CompanyInfo with given id does not exist.")
        self.__repo.update(c)
        return c
