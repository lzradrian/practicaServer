class InternshipService:
    def __init__(self, __repo):
        self.__repo = __repo

    def add(self, internship):
        internship_found = self.__repo.get_one(internship.id)
        if internship_found is not None:
            raise ValueError("Already exists a user with given id")
        return self.__repo.add(internship)

    def getAll(self):
        internships = self.__repo.get_all()
        return internships

    def getOne(self, id):
        internship = self.__repo.get_one(id)
        if internship is None:
            raise ValueError("User with given id does not exist.")
        return internship

    def get_by_representative_id(self, representative_id):
        internship = self.__repo.get_by_representative_id(representative_id)
        if internship is None:
            raise ValueError("User with given username does not exist.")
        return internship

    def remove(self, id):
        internship = self.__repo.get_one(id)
        if internship is None:
            raise ValueError("User with given id does not exist.")
        self.__repo.remove(internship)

    def update(self, internship):
        internship_found = self.__repo.get_one(internship.get_id())
        if internship_found is None:
            raise ValueError("User with given id does not exist.")
        self.__repo.update(internship)
        return internship
