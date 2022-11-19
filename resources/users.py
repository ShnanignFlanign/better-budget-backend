import models 

from flask import request, jsonify, Blueprint, session
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from flask_cors import CORS, cross_origin
from playhouse.shortcuts import model_to_dict
from datetime import timedelta



user = Blueprint('user', 'user')

@user.route('/signup', methods=["POST"])
# @cross_origin()
def register():
    payload = request.get_json()
    payload['email'] = payload['email'].lower()

    try:
        models.User.get(models.User.email == payload['email'])
        return jsonify(data={}, status={
            "code": 401, 
            "message": "A user with that name already exists"
        })
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password']) 
        user = models.User.create(**payload)

        login_user(user)

        user_dict = model_to_dict(user)
        print(user_dict)
        print(type(user_dict))

        del user_dict['password']

        return jsonify(
            data = user_dict,
            status = {
                "code": 201,
                "message": "Success"
            }
        )
    
@user.route('/login', methods=["POST"])
# @cross_origin()
def login():
    payload = request.get_json()
    try:
        user = models.User.get(models.User.email == payload['email']) 
        user_dict = model_to_dict(user) 
        if(check_password_hash(user_dict['password'], payload['password'])): 
            del user_dict['password'] 
            # session.permanent = True
            # login_user(user, remember=True, duration=timedelta(days=365), force=True) 
            login_user(user)
            print(f"'{current_user.username}' is current_user.username in POST register")
            return jsonify(data=user_dict, status={"code": 200, "message": "Success"}) 
        else:
            return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})


@user.route('/logout', methods=['GET'])
@login_required
# @cross_origin()
def logout():
    print(current_user.username)
    logout_user()
    return jsonify(
        data={},
        message="Successfully logged out.",
        status=200
    ), 200
