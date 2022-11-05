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
    user_id = ForeignKeyField(User, backref='Accounts')

    class Meta:
        database = DATABASE

class Transaction(Model):
    name = CharField()
    amount = DecimalField(default=0)
    category = CharField()
    description = TextField()
    date = datetime(default=datetime.datetime.now)
    acct_id = ForeignKeyField(Account, backref='Transactions')

def initialize(): 
    DATABASE.connect()

    DATABASE.create_tables([User, Account], safe=True)
    print('DB connection confirmed, created necessary tables.')

    DATABASE.close()