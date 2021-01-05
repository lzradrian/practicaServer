class StudentInternshipService:
    def __init__(self, __repo):
        self.__repo = __repo

    def add(self, student_internship):
        student_internship_found = self.__repo.get_one(student_internship.id)
        if student_internship_found is not None:
            raise ValueError("Already exists a user with given id")
        return self.__repo.add(student_internship)

    def getAll(self):
        student_internships = self.__repo.get_all()
        return student_internships

    def getOne(self, id):
        student_internship = self.__repo.get_one(id)
        if student_internship is None:
            raise ValueError("User with given id does not exist.")
        return student_internship

    def get_by_internship_id(self, internship_id):
        student_internship = self.__repo.get_by_internship_id(internship_id)
        if student_internship is None:
            raise ValueError("User with given username does not exist.")
        return student_internship

    def remove(self, id):
        student_internship = self.__repo.get_one(id)
        if student_internship is None:
            raise ValueError("User with given id does not exist.")
        self.__repo.remove(student_internship)

    def update(self, student_internship):
        student_internship_found = self.__repo.get_one(student_internship.get_id())
        if student_internship_found is None:
            raise ValueError("User with given id does not exist.")
        self.__repo.update(student_internship)
        return student_internship
