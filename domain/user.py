from main import db

class User(db.Model):
    #__tablename__ = 'Users'
    _id = db.Column("id",db.Integer,primary_key=True,autoincrement=True)
    username= db.Column(db.String)
    password = db.Column(db.String)
    email=db.Column(db.String)

    def __init__(self,id,username,password):
        self.id=id
        self.username=username
        self.password=password


    def set_id(self,value):
        self.id=value

    def set_name(self, value):
        self.username=value

    def set_email(self, value):
        self.email=value

    def set_password(self, value):
        self.password=value

    def get_id(self):
        return self.id

    def get_name(self):
        return self.username

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password
