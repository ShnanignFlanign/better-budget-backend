import models 
from flask import Blueprint, request, jsonify
from flask_login import current_user
from playhouse.shortcuts import model_to_dict

transactions = Blueprint('transactions', 'transactions')

@transactions.route('/<id>/transactions')
def trans_index(id):
    account = models.Account.get_by_id(id)
    print('result of select() query', account)
    trans_list = account.transactions
    acct_trans_dicts = [model_to_dict(trans) for trans in trans_list]

    for trans_dicts in acct_trans_dicts:
        trans_dicts.pop('acct_id')

    return jsonify({
        'data': acct_trans_dicts,
        'msg': f"found {len(acct_trans_dicts)} transactions",
        'status': 200
    }), 200

@transactions.route('/<id>/transactions', methods=['POST', 'PUT'])
def create_transaction(id):
    payload = request.get_json()
    new_trans = models.Transaction.create(acct_id=id, name=payload['name'], amount=payload['amount'], category=payload['category'], description=payload['description'])
    trans_dict = model_to_dict(new_trans)
    trans_dict['acct_id'].pop('user_id')

    account = models.Account.get_by_id(id)
    new_balance = account.balance - payload['amount']
    update_query = models.Account.update(balance=new_balance).where(models.Account.id == id)
    update_query.execute()
    
    return jsonify(
        data=trans_dict,
        message='transaction successfully created', 
        status=201
    ), 201

@transactions.route('/<aid>/transactions/<id>', methods=['PUT'])
def edit_transaction(aid, id):
    payload = request.get_json()
    query = models.Transaction.update(**payload).where(models.Transaction.id == id)
    query.execute()
    edited_trans = model_to_dict(models.Transaction.get_by_id(id))
    edited_trans.pop('acct_id')
    return jsonify(
        data = edited_trans,
        message = "updated transaction successfully",
        status = 200
    ), 200

@transactions.route('/<aid>/transactions/<id>', methods=['DELETE'])
def delete_transaction(aid, id):
    query = models.Transaction.delete().where(models.Transaction.id == id)
    query.execute()
    return jsonify(
        data = id,
        message = "Successfully deleted transaction",
        status = 200
    ), 200