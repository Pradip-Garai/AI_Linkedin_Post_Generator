from mongoengine import *

class Users(Document):
    name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    gender = StringField(required=True)
    occupation =  StringField(required=True)
    password = StringField(required=True, min_length=6)
    verified = BooleanField(default=False)

