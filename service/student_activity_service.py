class StudentActivityService:
    def __init__(self, __repo):
        self.__repo = __repo

    def add(self, student_activity):
        student_activity_found = self.__repo.get_one(student_activity.id)
        if student_activity_found is not None:
            raise ValueError("Already exists a StudentActivity with given id")
        return self.__repo.add(student_activity)

    def getAll(self):
        student_activitys = self.__repo.getAll()
        return student_activitys

    def getOne(self, id):
        student_activity = self.__repo.get_one(id)
        if student_activity is None:
            raise ValueError("StudentActivity with given id does not exist.")
        return student_activity

    def get_all_with_student_id(self, student_id):
        student_activities = self.__repo.get_all_with_student_id(student_id)
        if student_activities is None:
            raise ValueError("StudentActivity with given id does not exist.")
        return student_activities

    def remove(self, id):
        student_activity = self.__repo.getOne(id)
        if student_activity is None:
            raise ValueError("StudentActivity with given id does not exist.")
        self.__repo.remove(student_activity)

    def update(self, student_activity):
        student_activity_found = self.__repo.getOne(student_activity.get_id())
        if student_activity_found is None:
            raise ValueError("StudentActivity with given id does not exist.")
        self.__repo.update(student_activity)
        return student_activity
