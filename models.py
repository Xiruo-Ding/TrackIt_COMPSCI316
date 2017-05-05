from sqlalchemy import sql, orm
from app import db
import sys

#TODO Make foreign key's reference/redo primary keys. Plaid categories/schema have been removed


# Member is for demonstration...
class Team(db.Model):
    __tablename__ = 'team'
    teamid = db.Column('teamid', db.INTEGER, primary_key=True)
    sport = db.Column('sport', db.String(20))


#May have to add unique constraints.
class Member(db.Model):
    __tablename__ = 'member'
    uid = db.Column('uid', db.INTEGER, primary_key=True)
    firstname = db.Column('firstname', db.String(20))
    lastname = db.Column('lastname', db.String(20))
    loginpassword = db.Column('loginpassword', db.String(20))


class PartOfTeam(db.Model):
    __tablename__ = 'partOfTeam'
    uid = db.Column('uid', db.INTEGER, primary_key=True)
    teamid = db.Column('teamid', db.INTEGER)
    position = db.Column('position', db.String(20))
    year = db.Column('year', db.INTEGER)

class Player(db.Model):
    __tablename__ = 'player'
    uid = db.Column('uid', db.INTEGER, primary_key=True)
    gradyear = db.Column('gradyear', db.INTEGER)
    gender = db.Column('gender', db.INTEGER)

class Mentor(db.Model):
    __tablename__ = 'mentor'
    uid = db.Column('uid', db.INTEGER, primary_key=True)
    teamid = db.Column('teamid', db.INTEGER)
    title = db.Column('title', db.String(20))

# updates/intsert into
class AccountInfo(db.Model):
    __tablename__ = 'accountinfo'
    aid = db.Column('aid', db.INTEGER, primary_key=True)
    uid = db.Column('uid', db.INTEGER, primary_key=True)
    bankaccountnumber = db.Column('bankaccountnumber', db.Float)
    Type = db.Column('type', db.String(20))
    password = db.Column('password', db.String(20))

class Category(db.Model):
    __tablename__ = 'category'
    categoryid = db.Column('categoryid', db.INTEGER, primary_key=True)
    plaidcategory = db.Column('plaidcategory', db.String(20))
    plaidname = db.Column('plaidname', db.String(20))


class MetaCategory(db.Model):
    __tablename__ = 'metaCategory'
    plaidcategory = db.Column('plaidcategory', db.String(20), primary_key=True)
# updates/insert into
class Goal(db.Model):
    __tablename__ = 'goal'
    uid = db.Column('uid', db.INTEGER, primary_key=True)
    plaidcategory = db.Column('plaidcategory', db.String(20))
    amount = db.Column('amount', db.Float)
    begindate = db.Column('begindate', db.String(20))
    enddate = db.Column('enddate', db.String(20))
    isweekly = db.Column('isweekly', db.INTEGER)    
    ismonthly = db.Column('ismonthly', db.INTEGER)    

# updates/intsert into
class Transaction(db.Model):
    __tablename__ = 'transaction'
    transactionid = db.Column('transactionid', db.String(20), primary_key=True)
    dateoftransaction = db.Column('dateoftransaction', db.String(8))
    plaidcategory = db.Column('plaidcategory', db.String(20))
    amount = db.Column('amount', db.Float(10))
    plaidname = db.Column('plaidname', db.String(20))




