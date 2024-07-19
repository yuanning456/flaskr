# routes.py
from flask import Blueprint, request, jsonify
from .models import User, db
from .schemas import UserSchema

bp = Blueprint('routes', __name__)

@bp.route('/user', methods=['POST'])
def add_user():
    name = request.json['name']
    new_user = User(name)
    db.session.add(new_user)
    db.session.commit()
    return UserSchema.jsonify(new_user)

@bp.route('/user', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = UserSchema.dump(all_users)
    return jsonify(result)