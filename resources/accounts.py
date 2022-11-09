import models 
from flask import Blueprint, request, jsonify
from flask_login import current_user
from playhouse.shortcuts import model_to_dict

accounts = Blueprint('accounts', 'accounts')

@accounts.route('/')
def accts_index():
    
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

@accounts.route('/<id>/history')
def acct_hist(id):
    
    account = models.Account.get_by_id(id)
    print('result of select() query', account)

    trans_list = models.Transaction.select().where(models.Transaction.acct_id == account)
    acct_trans_dicts = [model_to_dict(account) for account in trans_list]

    # for trans_dicts in acct_trans_dicts:
    #     trans_dicts.pop('acct_id')
    
    deps_list = models.Deposit.select().where(models.Deposit.acct_id == account)
    acct_deps_dicts = [model_to_dict(account) for account in deps_list]

    # for deps_dicts in acct_deps_dicts:
    #     deps_dicts.pop('acct_id')

    total_dicts = acct_trans_dicts + acct_deps_dicts

    for dicts in total_dicts:
        dicts.pop('acct_id')

    return jsonify({
        'data': total_dicts,
        'msg': f"found {len(total_dicts)} account details.",
        'status': 200
    }), 200

@accounts.route('/<id>', methods=['PUT'])
def update_acct(id):
    payload = request.get_json()
    query = models.Account.update(**payload).where(models.Account.id == id) 
    query.execute()
    return jsonify(
        data = model_to_dict(models.Account.get_by_id(id)), 
        message="resource updated successfully",
        status=200
    ), 200

@accounts.route('/<id>', methods=['DELETE'])
def delete_acct(id):
    query = models.Account.delete().where(models.Account.id == id)
    query.execute()
    return jsonify(
        data = id,
        message = 'successfully deleted account',
        status = 200
    ), 200