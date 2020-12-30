class ConventieService:
    def __init__(self,__repo):
        self.__repo = __repo

    def add(self,conventie):
        conventiefound = self.__repo.getOne(conventie.get_id())
        if (conventiefound != None):
            raise ValueError("Already exists a conventie with given id")
        return self.__repo.add(conventie)

    def getAll(self):
        conventii =  self.__repo.getAll()
        return conventii

    def getOne(self,id):
        conventie = self.__repo.getOne(id)
        if(conventie==None):
            raise ValueError("Conventie with given id does not exist.")
        return conventie

    def remove(self,id):
        conventie = self.__repo.getOne(id)
        if (conventie == None):
            raise ValueError("Conventie with given id does not exist.")
        self.__repo.remove(conventie)

    def update(self,conventie):
        conventiefound = self.__repo.getOne(conventie.get_id())
        if (conventiefound == None):
            raise ValueError("Conventie with given id does not exist.")
        self.__repo.update(conventie)
        return conventie
