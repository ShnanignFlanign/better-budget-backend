import models 
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict
from decimal import Decimal

transactions = Blueprint('transactions', 'transactions')

@transactions.route('/<id>/transactions')
@login_required
def trans_index(id):
    account = models.Account.get_by_id(id)
    print('result of select() query', account)
    trans_list = account.transactions
    acct_trans_dicts = [model_to_dict(trans) for trans in trans_list]

    for trans_dicts in acct_trans_dicts:
        trans_dicts.pop('acct_id')
    
    sorted_total = sorted(acct_trans_dicts, key=lambda d: d['date'])

    return jsonify({
        'data': sorted_total,
        'msg': f"found {len(acct_trans_dicts)} transactions",
        'status': 200
    }), 200

@transactions.route('/<id>/transactions', methods=['POST'])
@login_required
def create_transaction(id):
    payload = request.get_json()
    new_trans = models.Transaction.create(acct_id=id, name=payload['name'], amount=payload['amount'], category=payload['category'], description=payload['description'])

    account = models.Account.get_by_id(id)
    new_balance = account.balance - Decimal(payload['amount'])
    update_query = models.Account.update(balance=new_balance).where(models.Account.id == id)
    update_query.execute()

    trans_dict = model_to_dict(new_trans)
    trans_dict['acct_id'].pop('user_id')

    return jsonify(
        data=trans_dict,
        message='transaction successfully created', 
        status=201
    ), 201

@transactions.route('/<aid>/transactions/<id>', methods=['PUT'])
@login_required
def edit_transaction(aid, id):
    payload = request.get_json()
    account = models.Account.get_by_id(aid)
    foundTrans = models.Transaction.get_by_id(id)
    
    new_balance = account.balance + (foundTrans.amount - Decimal(payload['amount']))
    acct_update = models.Account.update(balance=new_balance).where(models.Account.id == aid)
    query = models.Transaction.update(**payload).where(models.Transaction.id == id)
    acct_update.execute()
    query.execute()

    edited_trans = model_to_dict(models.Transaction.get_by_id(id))
    edited_trans.pop('acct_id')
    return jsonify(
        data = edited_trans,
        message = "updated transaction successfully",
        status = 200
    ), 200

@transactions.route('/<aid>/transactions/<id>', methods=['DELETE'])
@login_required
def delete_transaction(aid, id):
    query = models.Transaction.delete().where(models.Transaction.id == id)
    query.execute()
    return jsonify(
        data = id,
        message = "Successfully deleted transaction",
        status = 200
    ), 200