class UserRepository:
    def getAll(self):
        from domain.user import User
        users = User.query.all()
        return users

    def getOne(self, id):
        from domain.user import User
        user = User.query.get(id)
        return user

    def getOneByUsername(self, id):
        from domain.user import User
        user = User.query.filter_by(username=id).first()
        return user

    def add(self, user):
        from controller import db
        db.session.add(user)
        db.session.commit()
        return user

    def remove(self, user):
        from controller import db
        db.session.delete(user)
        db.session.commit()

    def update(self, user):
        from controller import db
        from domain.user import User
        userfound = User.query.get(user.get_id())
        userfound.set_usernamename(user.get_username())
        userfound.set_email(user.get_email())
        userfound.set_password(user.get_password())
        db.session.commit()
        return user
