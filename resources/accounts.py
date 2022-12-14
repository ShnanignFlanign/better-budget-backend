import models 
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict

accounts = Blueprint('accounts', 'accounts')

@accounts.route('/')
@login_required
def accts_index():
    print(current_user)
    result = models.Account.select()
    print('result of select() query', result)
    print(f"'{current_user.username}' is current_user.username in acct GET")
    current_user_acct_dicts = [model_to_dict(account) for account in current_user.accounts]

    for acct_dict in current_user_acct_dicts:
        acct_dict['user_id'].pop('password')

    return jsonify({
        'data': current_user_acct_dicts,
        'msg': f"found {len(current_user_acct_dicts)} accounts.",
        'status': 200
    }), 200

@accounts.route('/', methods=['POST'])
@login_required
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
@login_required
def acct_hist(id):
    account = models.Account.get_by_id(id)
    print('result of select() query', account)

    # trans_list = account.transactions
    trans_list = models.Transaction.select().where(models.Transaction.acct_id == id)
    acct_trans_dicts = [model_to_dict(trans) for trans in trans_list] 
    for trans in acct_trans_dicts:
        trans['type'] = 'transaction'

    deps_list = models.Deposit.select().where(models.Deposit.acct_id == id)
    acct_deps_dicts = [model_to_dict(dep) for dep in deps_list]
    for deps in acct_deps_dicts:
        deps['type'] = 'deposit'

    total_dicts = acct_trans_dicts + acct_deps_dicts
    for dicts in total_dicts:
        dicts.pop('acct_id')
    #change this to return one sorted list. Once changed, change fetch call on front end.
    sorted_total = sorted(total_dicts, key=lambda d: d['date'])
    # sorted_trans = sorted(acct_trans_dicts, key=lambda d: d['date'])
    # sorted_deps = sorted(acct_deps_dicts, key=lambda d: d['date'])

    return jsonify({
        'data': {
            'History': sorted_total
        },
        'msg': f"found {len(sorted_total)} account details.",
        'status': 200
    }), 200

@accounts.route('/<id>', methods=['PUT'])
@login_required
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
@login_required
def delete_acct(id):
    account = models.Account.get_by_id(id)
    del_deps = models.Deposit.delete().where(models.Deposit.acct_id == id)
    del_trans = models.Transaction.delete().where(models.Transaction.acct_id == id)
    query = models.Account.delete().where(models.Account.id == id)
    del_deps.execute()
    del_trans.execute()
    query.execute()
    return jsonify(
        data = id,
        message = 'successfully deleted account',
        status = 200
    ), 200