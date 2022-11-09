import models 
from flask import Blueprint, request, jsonify
from flask_login import current_user
from playhouse.shortcuts import model_to_dict

deposits = Blueprint('deposits', 'deposits')

@deposits.route('/<id>/deposits')
def trans_index(id):
    account = models.Account.get_by_id(id)
    print('result of select() query', account)
    deps_list = account.deposits
    acct_deps_dicts = [model_to_dict(dep) for dep in deps_list]

    for deps_dicts in acct_deps_dicts:
        deps_dicts.pop('acct_id')

    return jsonify({
        'data': acct_deps_dicts,
        'msg': f"found {len(acct_deps_dicts)} deposits",
        'status': 200
    }), 200

@deposits.route('/<id>/deposits', methods=['POST'])
def create_transaction(id):
    payload = request.get_json()
    new_dep = models.Deposit.create(acct_id=id, name=payload['name'], amount=payload['amount'])

    account = models.Account.get_by_id(id)
    new_balance = account.balance + payload['amount']
    update_query = models.Account.update(balance=new_balance).where(models.Account.id == id)
    update_query.execute()

    dep_dict = model_to_dict(new_dep)
    dep_dict['acct_id'].pop('user_id')

    return jsonify(
        data=dep_dict,
        message='deposit successfully created', 
        status=201
    ), 201

@deposits.route('/<aid>/deposits/<id>', methods=['PUT'])
def edit_transaction(aid, id):
    payload = request.get_json()
    account = models.Account.get_by_id(aid)
    deposit = models.Deposit.get_by_id(id)
    
    new_balance = account.balance - (deposit.amount - payload['amount'])
    acct_update = account.update(balance=new_balance)
    query = deposit.update(**payload)
    acct_update.execute()
    query.execute()
    edited_dep = model_to_dict(models.Deposit.get_by_id(id))
    edited_dep.pop('acct_id')
    return jsonify(
        data = edited_dep,
        message = "updated deposit successfully",
        status = 200
    ), 200

@deposits.route('/<aid>/deposits/<id>', methods=['DELETE'])
def delete_transaction(aid, id):
    query = models.Deposit.delete().where(models.Deposit.id == id)
    query.execute()
    return jsonify(
        data = id,
        message = "Successfully deleted deposit",
        status = 200
    ), 200