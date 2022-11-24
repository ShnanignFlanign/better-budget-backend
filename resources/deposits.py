import models 
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict
from decimal import Decimal

deposits = Blueprint('deposits', 'deposits')

@deposits.route('/<id>/deposits')
@login_required
def deps_index(id):
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
@login_required
def create_deposit(id):
    payload = request.get_json()
    new_dep = models.Deposit.create(acct_id=id, name=payload['name'], amount=payload['amount'])

    account = models.Account.get_by_id(id)
    new_balance = account.balance + Decimal(payload['amount'])
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
@login_required
def edit_deposit(aid, id):
    payload = request.get_json()
    account = models.Account.get_by_id(aid)
    deposit = models.Deposit.get_by_id(id)

    new_balance = account.balance - (deposit.amount - Decimal(payload['amount']))
    acct_update = models.Account.update(balance=new_balance).where(models.Account.id == id)
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
@login_required
def delete_deposit(aid, id):
    query = models.Deposit.delete().where(models.Deposit.id == id)
    query.execute()
    return jsonify(
        data = id,
        message = "Successfully deleted deposit",
        status = 200
    ), 200