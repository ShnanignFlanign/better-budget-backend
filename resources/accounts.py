import models 
from flask import Blueprint, request, jsonify
from flask_login import current_user
from playhouse.shortcuts import model_to_dict

accounts = Blueprint('accounts', 'accounts')

@accounts.route('/')
def dogs_index():
    
    result = models.Account.select()
    print('result of select() query', result)

    current_user_acct_dicts = [model_to_dict(account) for account in current_user.accounts]

    for acct_dict in current_user_acct_dicts:
        acct_dict['user_id'].pop('password')

    return jsonify({
        'data': current_user_acct_dicts,
        'msg': f"found {len(current_user_acct_dicts)} accounts.",
        'status': 200
    }), 200

@accounts.route('/', methods=['POST'])
def create_acct():
    payload = request.get_json()
    print(payload)
    new_acct = models.Account.create(name=payload['name'], user_id = current_user.id, balance = payload['balance'])
    print(new_acct)
    acct_dict = model_to_dict(new_acct)
    acct_dict['user_id'].pop('password')

    return jsonify(
        data=acct_dict, 
        message='account successfully created', 
        status=201
    ), 201