class UserService:
    def __init__(self, __repo):
        self.__repo = __repo

    def add(self, user):
        user_found = self.__repo.getOne(user.get_id(), user.get_id())
        if user_found is not None:
            raise ValueError("Already exists a user with given id")
        return self.__repo.add(user)

    def getAll(self):
        users = self.__repo.getAll()
        return users

    def getOne(self, id):
        user = self.__repo.getOne(id)
        if user is None:
            raise ValueError("User with given id does not exist.")
        return user

    def getOneByUsername(self, id):
        user = self.__repo.getOneByUsername(id)
        if user is None:
            raise ValueError("User with given username does not exist.")
        return user

    def remove(self, id):
        user = self.__repo.getOne(id)
        if user is None:
            raise ValueError("User with given id does not exist.")
        self.__repo.remove(user)

    def update(self, user):
        user_found = self.__repo.getOne(user.get_id())
        if user_found is None:
            raise ValueError("User with given id does not exist.")
        self.__repo.update(user)
        return user
