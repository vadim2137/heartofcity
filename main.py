from flask import  Flask, render_template, request, redirect, url_for, flash, make_response, session
from flask import session
import sqlite3 as sql
from DBUtils import DataBase
import datetime
import os
from werkzeug.utils import secure_filename
from PIL import Image



app = Flask(__name__)
app.permanent_session_lifetime = datetime.timedelta(days=30)
app.config["SECRET_KEY"] = "vadim2137"


@app.route('/', methods=['GET', 'POST'])
def index():
    testtolog = 0
    try:
        firstname = session['user']['firstname']
        surname = session['user']['surname']
    except:
        firstname = "balabolikiz"
        surname = "barashek"
    print(session.items())
    db = DataBase(sql.connect("database.db"))
    if request.method == "POST":
        try:
            firstname = request.form.get('firstname')
            surname = request.form.get('surname')
            pnumber = request.form.get('phonenumber')
            password = request.form.get('password')
            Trues, firstname, surname, password, phonenumber, idu = db.CreateNewUser(firstname, surname, password, pnumber)
        except:
            pnumber = request.form.get('pnumber')
            password = request.form.get('password')
            print(pnumber, "BLAT")
            Trues, firstname, surname, idu = db.LoginUser(pnumber, password)
            testtolog = 1
        
        if Trues == True:
            try:
                session['user']['firstname'] = firstname
                session['user']['surname'] = surname
                session['user']['id'] = idu
            except:
                session['user'] = {'firstname': firstname,
                                   'surname': surname,
                                   'id': idu}
        else:
             return render_template("index.html")
    return render_template("index.html", firstname=firstname, surname=surname)

@app.route('/idea', methods=['GET', 'POST'])
def idea():
    db = DataBase(sql.connect("database.db"))
    check = request.args.get('key')
    Trues = 0
    try:
        firstname = session['user']['firstname']
        surname = session['user']['surname']
    except:
        firstname = "balabolikiz"
        surname = "barashek"
        check = 1
    if request.method == 'POST':
        print(request.files)
        if check == "1":
            photo = request.form.get('photo')
            description = request.form.get('description')
            title = request.form.get('title')
            file = request.files['photo']
            print(firstname, surname)
            filename = secure_filename(file.filename)
            file.save(os.path.join("static//images//ideas//", f"{surname}_{title}.png"))
            db.AddIdea(title, description, f"{surname}_{title}.png", f"{firstname}_{surname}")
        elif check == None:
            pnumber = request.form.get('phonenumber')
            password = request.form.get('password')
            Trues, firstname, surname, idu = db.LoginUser(pnumber, password)

        if Trues == True:
            try:
                session['user']['firstname'] = firstname
                session['user']['surname'] = surname
            except:
                session['user'] = {'firstname': firstname,
                                   'surname': surname}
    
    return render_template('suggestidea.html', firstname=firstname, surname=surname)

app.run('localhost', debug = False)


