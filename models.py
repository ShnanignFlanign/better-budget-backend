from peewee import * 
import datetime 
from flask_login import UserMixin

DATABASE = SqliteDatabase('budget.sqlite')

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE

class Account(Model):
    name = CharField()
    balance = DecimalField(default=0)
    user_id = ForeignKeyField(User, backref='accounts')

    class Meta:
        database = DATABASE

class Transaction(Model):
    name = CharField()
    amount = DecimalField(default=0)
    category = CharField()
    description = TextField()
    date = DateTimeField(default=datetime.datetime.now)
    acct_id = ForeignKeyField(Account, backref='transactions')

    class Meta:
        database = DATABASE

class Deposit(Model):
    name = CharField()
    amount = DecimalField(default=0)
    date = DateTimeField(default=datetime.datetime.now)
    acct_id = ForeignKeyField(Account, backref='deposits')

    class Meta:
        database = DATABASE

def initialize(): 
    DATABASE.connect()

    ##ADD ACCOUNT AND TRANSACTION TABLES HERE ONCE FIGURED OUT 
    DATABASE.create_tables([Account, Deposit, Transaction, User], safe=True)
    print('DB connection confirmed, created necessary tables.')

    DATABASE.close()