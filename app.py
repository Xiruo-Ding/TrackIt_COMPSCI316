from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
import models
import forms
from sqlalchemy import create_engine
from sqlalchemy.sql import text

app = Flask(__name__)
app.secret_key = 's3cr3t'
app.config.from_object('config')
db = SQLAlchemy(app, session_options={'autocommit': False})

dbe = create_engine("postgresql://vagrant:dbpasswd@localhost/trackit")

uid = -1


@app.route('/', methods=['GET','POST'])
def login():
    error = None

    if request.method == 'POST':
        global uid
        uid = request.form['username']

        cmd = 'SELECT loginpassword FROM Member WHERE uid = :uid'
        connection = dbe.connect()
        actualpwd = connection.execute(text(cmd), {'uid':uid})
        pwdTest = actualpwd.fetchone()['loginpassword']
        


        if  request.form['password'] != pwdTest:
            error = True 
        elif int(uid) >= 1 and int(uid) <= 50:
            return redirect(url_for('player_hm'))
        else:
            return redirect(url_for('coach_hm'))
    
    
    return render_template('login.html', error=error)




@app.route('/player')
def player_hm():
    #members = db.session.query(models.Member).all()
    #trans = db.session.query(models.Transaction).all()

    
    cmd = 'SELECT t.dateoftransaction, t.plaidName, t.plaidCategory, t.amount FROM playertransactions as t WHERE t.uid = :loginUid GROUP BY t.dateoftransaction, t.plaidName, t.plaidCategory, t.amount ORDER BY t.dateoftransaction DESC'
    result = db.engine.execute( text(cmd), {'loginUid': uid}).fetchall()

    connection = dbe.connect()
    
    cmd2 = 'SELECT DISTINCT firstname FROM member WHERE uid = :loginUid '
    firstname = connection.execute(text(cmd2), {'loginUid': uid})
    actualfirstname = firstname.fetchone()['firstname']
    
    cmd3 = 'SELECT DISTINCT lastname FROM member WHERE uid = :loginUid '
    lastname = connection.execute(text(cmd3), {'loginUid': uid})
    actuallastname = lastname.fetchone()['lastname']

    name = actualfirstname + " " + actuallastname


    # budget
    cmd4 = 'SELECT p.plaidCategory, p.beginDate, p.endDate, p.goalAmount, p.actualAmount, p.isWeekly FROM playerReport as p WHERE p.uid = :loginUid GROUP BY p.plaidCategory, p.beginDate, p.endDate, p.goalAmount, p.actualAmount, p.isWeekly'   
    budget = db.engine.execute(text(cmd4),{'loginUid': uid}).fetchall()
    
    return render_template('player-home.html', budget = budget[0:10], trans = result[0:10], name=name)


@app.route('/coach', methods = ['GET', 'POST'])
def coach_hm():

    if request.method == 'POST':
        print('ddd')


    connection = dbe.connect()
        
    cmd2 = 'SELECT teamid FROM Mentor WHERE Mentor.uid = :loginUid'
    tid = connection.execute(text(cmd2), {'loginUid' : uid})
    realTID = tid.fetchone()['teamid']

    cmd ='SELECT p.uid, p.plaidCategory, p.isWeekly, p.goalAmount, p.actualAmount FROM playerReport p WHERE p.uid IN (SELECT PartOfTeam.uid FROM Team, PartOfTeam WHERE Team.teamID = :fuckyouid AND PartOfTeam.teamID = Team.teamID)'

    budgets = connection.execute(text(cmd), {'fuckyouid': realTID})    

    return render_template('coach_home.html', budgets = budgets)


@app.route('/transaction')
def transac():
    cmd = 'SELECT t.dateoftransaction, t.plaidName, t.plaidCategory, t.amount FROM playertransactions as t WHERE t.uid = :loginUid GROUP BY t.dateoftransaction, t.plaidName, t.plaidCategory, t.amount ORDER BY t.dateoftransaction DESC'
    result = db.engine.execute( text(cmd), {'loginUid': uid}).fetchall()
    return render_template('transactions.html', trans = result)


@app.route('/budget')
def bdg():


    cmd4 = 'SELECT p.plaidCategory, p.beginDate, p.endDate, p.goalAmount, p.actualAmount, p.isWeekly FROM playerReport as p WHERE p.uid = :loginUid GROUP BY p.plaidCategory, p.beginDate, p.endDate, p.goalAmount, p.actualAmount, p.isWeekly'   
    budget = db.engine.execute(text(cmd4),{'loginUid': uid}).fetchall()

    return render_template('budgets.html', budget = budget)

@app.route('/new-bdg', methods = ['GET','POST'])
def new_bdg():

    if request.method == 'POST':
        plaidCategory = request.form['category']
        amount = request.form['budget']
        tp = request.form['type']
        date = request.form['start-date']


        if(tp == 'Monthly'):
            isMonthly = 1
            isWeekly = 0
        else:
            isMonthly = 0
            isWeekly = 1

        date_start = date[0:10]
        date_end = date[11:]  
        connection = dbe.connect()
        # recommended
        cmd = 'INSERT INTO Goal VALUES(:uid, :plaidCategory , :amount, :beginDate, :endDate, :isWeekly, :isMonthly)'
        result = connection.execute(text(cmd), {'uid' : uid , 'plaidCategory' : plaidCategory , 'amount' : amount, 'beginDate' : date_start, 'endDate' : date_end,'isWeekly' : isWeekly, 'isMonthly' : isMonthly})

       # print("::::::::::::::::::::::")
       ##print(plaidCategory)
       # print(amount)
       # print(tp)
       # print(isMonthly)
       # print(isWeekly)
       # print(date)
       # print(date_start)
       # print(date_end)

    return render_template('new-budget.html')


@app.route('/add-account', methods = ['GET', 'POST'])
def add_acct():
    if request.method == 'POST':

        pwd = request.form['password']
        acc_no = request.form['acc-num']
        acc_nm = request.form['acc-name']
        

        aid = int(str(uid) + str(acc_no))

        connection = dbe.connect()
        cmd = 'INSERT INTO AccountInfo Values(:aid, :uid, :bankAccountNumber, :Type, :password )'
        result = connection.execute(text(cmd), {'aid' : aid, 'uid' : uid, 'bankAccountNumber' : acc_no, 'password' : pwd, 'Type' : acc_nm})
        return redirect(url_for('player_hm'))
    return render_template('add-account.html')






@app.template_filter('pluralize')
def pluralize(number, singular='', plural='s'):
    return singular if number in (0, 1) else plural

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
