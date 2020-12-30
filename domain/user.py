from controller import db


class User(db.Model):
    __tablename__ = 'Users'
    _id = db.Column("id",db.Integer,primary_key=True,autoincrement=True)
    username= db.Column("username",db.String)
    password = db.Column("password",db.String)
    email=db.Column("email",db.String)
    role = db.Column('role', db.SmallInteger)

    def __init__(self,id,username,password,email,role):
        self.id=id
        self.username=username
        self.password=password
        self.email=email
        self.role=role

    def set_id(self,value):
        self.id=value

    def set_name(self, value):
        self.username=value

    def set_email(self, value):
        self.email=value

    def set_password(self, value):
        self.password=value

    def set_role(self,value):
        self.role=value

    def get_id(self):
        return self.id

    def get_name(self):
        return self.username

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password

    def get_role(self):
        return self.role