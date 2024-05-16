"""
Routes and views for the flask application.


import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from sqlalchemy.exc import IntegrityError
import bcrypt
from flask import Flask, flash, render_template, request, url_for, redirect,session
from flask import app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, utils
from flask_bcrypt import Bcrypt
from flask import session
from flask_session import Session
"""

app = Flask(__name__, template_folder="templates")


conn = sqlite3.connect("db.sqlite3", check_same_thread=False)
c = conn.cursor()

app = Flask(__name__)
app.config["SECRET_KEY"] = "sadfg447kafgd"



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if the form is valid
        email = request.form['email']
        password = request.form['password']
        confirmation = request.form['confirmation']

        if not email or not password or not confirmation:
            return "please fill out all fields"

        if password != confirmation:
                return "password confirmation doesn't match password"

            # check if email exist in the database
        sql = f"SELECT * FROM users WHERE email='{email}'"
        res = c.execute(sql)
        rows = res.fetchall()

        if len(rows) != 0:
            return "user already registered"

            # hash the password
        pwhash = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)

            # insert the row
        c.execute(f"INSERT INTO users (email, password) VALUES ('{email}', '{pwhash}')")
        conn.commit()

            # return success
        return "registered successfully!"
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check the form is valid
        if not request.form.get("email") or not request.form.get("password"):
            return "please fill out all required fields"

        # check if email exist in the database
        user = c.execute("SELECT * FROM users WHERE email=:email", {"email": request.form.get("email")}).fetchall()

        if len(user) != 1:
            return "you didn't register"

        # check the password is same to password hash
        pwhash = user[0][2]
        if check_password_hash(pwhash, request.form.get("password")) == False:
            return "wrong password"

        # login the user using session
        session["user_id"] = user[0][0]

        # return success

        user_id = session['user_id']

        print(user_id)

        return render_template("client.html")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))



@app.route('/')
def start():
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] !='admin':
            error = 'Invalid user name or password. Please try again'
        else: flash('You were successfully logged in')
        return redirect(url_for('client'))
    return render_template('signin.html', error=error)

@app.route('/signout')
def signout():
    return redirect(url_for('signin'))



@app.route('/plot/<number>')
def check_plot_number(number):
    return " "


@app.route('/rem')
@login_required
def rem():
    """Renders the home page."""
    return render_template(
'rem.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
'index.html',
        title='Home Page',
        year=datetime.now().year,
    )


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )


@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )


@app.route('/client')
def client():
    """Renders the about page."""
    return render_template(
        'client.html',
        title='Client',
        year=datetime.now().year,
        message='Client Plot Booking.'
    )


@app.route('/rehodata', methods = ['POST','GET'])
def rehodata():
    if request.method == 'POST':
        info = request.form
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone = request.form['phone']
        email = request.form['email']
        plot_number = request.form['plot_number']
        price = request.form['price']

        client_dict = [{'First Name':first_name,'Last Name':last_name, 'Phone':phone, 'Email': email,
                        'Plot Number':plot_number,'Price':price  }]

        print(client_dict)

        try:
            with sqlite3.connect('clients_x_db.db') as conx:
                curr = conx.cursor()
                sql = (f"INSERT INTO clients(`first_name`, `last_name`, `phone`, `email`, `plot_number`, `price`) "
                       f"VALUES('{first_name}','{last_name}','{phone}','{email}','{plot_number}','{price}')")
                curr.execute(sql)
                conx.commit()

        except sqlite3.Error as e:

            print(e)
            print(client_dict)
        return render_template('table.html', info = info)


@app.route('/delt', methods=['POST', 'GET'])
def delt():
    if request.method == 'POST':
        info=request.form
        plot_number = request.form['plot_number']
        plot_number= int(plot_number)
        try:
            with sqlite3.connect('clients_x_db.db') as con:
                curr = con.cursor()
                sql = f"DELETE FROM clients WHERE plot_number= '{plot_number}'"
                curr.execute(sql)
                con.commit()
               # return render_template('list.html')
                conx=sqlite3.connect('clients_x_db.db')
                curr2 = conx.cursor()
                sql1 = f"SELECT * FROM clients"
                conx.row_factory = sqlite3.Row
                curr2.execute(sql1)
                rows = curr2.fetchall()

                info ="Deleted"

                return render_template("list.html", rows=rows)
        except sqlite3.Error as e:
            print(e)
    else:
        return render_template("list.html", info =info)

@app.route('/client_list')
def client_list():
    try:
       with sqlite3.connect('clients_x_db.db') as con:
            conx=sqlite3.connect('clients_x_db.db')
            curr2 = conx.cursor()
            sql1 = f"SELECT * FROM clients"
            conx.row_factory = sqlite3.Row
            curr2.execute(sql1)
            rows = curr2.fetchall()

            info = "Client List"

            return render_template("client_list.html", rows=rows)

    except sqlite3.Error as e:
        print(e)
        return render_template("list.html", info =info)


if __name__ == '__main__':
        app.run(host="127.0.0.1")