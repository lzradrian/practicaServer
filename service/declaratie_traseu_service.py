class DeclaratieTraseuService:
    def __init__(self, __repo):
        self.__repo = __repo

    def add(self, declaratie):
        declaratie_found = self.__repo.getOne(declaratie.student_id)
        if declaratie_found is not None:
            raise ValueError("A declaration with the given ID already exists!")
        return self.__repo.add(declaratie)

    def getAll(self):
        declaratii = self.__repo.getAll()
        return declaratii

    def getOne(self, id):
        declaratie = self.__repo.getOne(id)
        if declaratie is None:
            raise ValueError("A declaration with the given ID does not exist!")
        return declaratie

    def remove(self, id):
        declaratie = self.__repo.getOne(id)
        if declaratie is None:
            raise ValueError("A declaration with the given ID does not exist!")
        self.__repo.remove(declaratie)

    def update(self, declaratie):
        declaratie_found = self.__repo.getOne(declaratie.student_id)
        if declaratie_found is None:
            raise ValueError("A declaration with the given ID does not exist!")
        self.__repo.update(declaratie)
        return declaratie
