# schemas.py
from marshmallow_sqlalchemy import ModelSchema
from .models import User

class UserSchema(ModelSchema):
    class Meta:
        model = User
        sqla_session = db.session

user_schema = UserSchema()
users_schema = UserSchema(many=True)