class UserService:
    def __init__(self,__repo):
        self.__repo = __repo

    def add(self,user):
        userfound = self.__repo.getOne(user.get_id())
        if (userfound != None):
            raise ValueError("Already exists a user with given id")
        return self.__repo.add(user)

    def getAll(self):
        users =  self.__repo.getAll()
        return users

    def getOne(self,id):
        user = self.__repo.getOne(id)
        if(user==None):
            raise ValueError("User with given id does not exist.")
        return user

    def getOneByUsername(self,id):
        user = self.__repo.getOneByUsername(id)
        if(user==None):
            raise ValueError("User with given username does not exist.")
        return user

    def remove(self,id):
        user = self.__repo.getOne(id)
        if (user == None):
            raise ValueError("User with given id does not exist.")
        self.__repo.remove(user)

    def update(self,user):
        userfound = self.__repo.getOne(user.get_id())
        if (userfound == None):
            raise ValueError("User with given id does not exist.")
        self.__repo.update(user)
        return user
