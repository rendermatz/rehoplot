"""
Routes and views for the flask application.
"""
import sqlite3
from datetime import datetime
from flask import Flask, flash, render_template, request, url_for, redirect, session
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="templates")


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///rehoplotdb.sqlite"

app.config["SECRET_KEY"] = "sadfg!@#447kafgd"

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)


db.init_app(app)


with app.app_context():
    db.create_all()


@login_manager.user_loader
def loader_user(user_id):
    return db.session.get(Users, user_id)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = Users()
        user.username = request.form["username"]
        user.password = request.form["password"]

        db.session.add(user)

        db.session.commit()

        return redirect(url_for("login"))

    return render_template("index.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = (Users.query.filter_by
                (username=request.form.get("email")).first())
        print(user.username)
        if user.password == request.form.get("password"):
            login_user(user)
        return redirect(url_for("client"))

    return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template("index.html")


@app.route('/')
def start():
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    message = "none"
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            message = "Invalid user name or password. Please try again"
            print(message)
        else:
            flash('You were successfully logged in')
        return redirect(url_for('client'))

    return render_template('signin.html', message=message)


@app.route('/signout')
def signout():
    session.clear()
    return redirect(url_for('signin'))


@app.route('/faraba/<number>')
def check_plot_number(number):
    number1 = number
    plotnumber = int(number1)
    if 0 > plotnumber < 200:
        con = sqlite3.connect("clients_x_db.db")
        curx = con.cursor()
        sql = f"SELECT * FROM clients"
        con.row_factory = sqlite3.Row
        res = curx.execute(sql)
        rows = res.fetchall()
        print(type(rows))
        for row in rows:
            print(row[0], row[1], row[2])

            if row[4] == plotnumber:
                return "This plot is not available"

    elif plotnumber <= 0 or plotnumber > 199:
        return "Please enter an available number"

    else:
        return "This plot is available"


@app.route('/rem')
@login_required
def rem():
    """Renders the home page."""
    return render_template(
        'rem.html',
        itle='Home Page', year=datetime.now().year,
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
@login_required
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
@login_required
def client():
    """Renders the about page."""
    return render_template(
        'client.html',
        title='Client',
        year=datetime.now().year,
        message='Client Plot Booking.'
    )

@app.route('/registration')
def registration():
    """Renders the about page."""
    return render_template(
        'register.html',
        title='Registration',
        year=datetime.now().year,
        message='Registration.'
    )


@app.route('/rehodata', methods=['POST', 'GET'])
def rehodata():
    if request.method == 'POST':
        info = request.form
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone = request.form['phone']
        email = request.form['email']
        plot_number = request.form['plot_number']
        price = request.form['price']

        client_dict = [{'First Name': first_name, 'Last Name': last_name, 'Phone': phone, 'Email': email,
                        'Plot Number': plot_number, 'Price': price}]

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
        return render_template('table.html', info=info)


@app.route('/delt', methods=['POST', 'GET'])
def delt():
    if request.method == 'POST':

        plot_number = request.form['plot_number']
        plot_number = int(plot_number)
        try:
            with sqlite3.connect('clients_x_db.db') as con:
                curr = con.cursor()
                sql = f"DELETE FROM clients WHERE plot_number= '{plot_number}'"
                curr.execute(sql)
                con.commit()
                # return render_template('list.html')

                conx = sqlite3.connect('clients_x_db.db')
                curr2 = conx.cursor()
                sql1 = f"SELECT * FROM clients"
                conx.row_factory = sqlite3.Row
                curr2.execute(sql1)
                rows = curr2.fetchall()

                return render_template("list.html", rows=rows)
        except sqlite3.Error as e:
            print(e)
    else:
        info = "Deleted"
        return render_template("list.html", info=info)


@app.route('/client_list')
def client_list():
    try:
        conx = sqlite3.connect('clients_x_db.db')
        curr2 = conx.cursor()
        sql1 = f"SELECT * FROM clients"
        conx.row_factory = sqlite3.Row
        curr2.execute(sql1)
        rows = curr2.fetchall()

        return render_template("client_list.html", rows=rows)

    except sqlite3.Error as e:
        print(e)
        info = "Client List"
    return render_template("list.html", info=info)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port = "10000", debug=True)
