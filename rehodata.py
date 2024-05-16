import sqlite3
from flask import Flask, render_template, request,app
from datetime import *


app = Flask(__name__, template_folder="templates")


@app.route('/')
def start():
    return "Hello"


try:
    conn= sqlite3.connect('clients_x_db.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE clients(first_name TEXT, last_name TEXT, phone INT, email TEXT, plot_number INT,
     price FLOAT)''')
    
except sqlite3.Error as e:
    print("database exists")
    print("Connected to database")


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
    return render_template('contact.html', title='Contact', year=datetime.now().year,message='Your contact page.'
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


@app.route('/rehodata', methods=['POST','GET'])
def rehodata():
    if request.method == 'POST':
        info = request.form
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone = request.form['phone']
        email = request.form['email']
        plot_number = request.form['plot_number']
        price = request.form['price']
        
        client_dict = {'First Name':first_name,'Last Name':last_name, 'Phone':phone, 'Email': email, 'Plot Number':plot_number,'Price':price  }
        
        try:
            with sqlite3.connect('clients_x_db.db') as conn:
                curr = conn.cursor()
                sql = f'''INSERT INTO clients(`first_name`, `last_name`, `phone`, `email`, `plot_number`, `price`) 
                VALUES('{first_name}','{last_name}','{phone}','{email}','{plot_number}','{price}')'''
                curr.execute(sql)
                conn.commit()
            
        except sqlite3.Error as e:

            print(e)
            print(client_dict)
        return render_template('table.html', info=info)



@app('/remove', methods= ['POST', 'GET'])
def remove():
    if request.method == 'POST':
        plot_number = request.form["plot_number"]
        plot_number= int(plot_number)
    try:
        with sqlite3.connect('clients_x_db.db') as con:
            curr = con.cursor()
            sql = f'''DELETE FROM clients WHERE `plot_number`='{plot_number}' '''
            sql1 = f"SELECT * FROM clients"
            curr.execute(sql,sql1)
            con.row_factory = sqlite3.Row
            con.commit()
            rows = curr.fetchall()

    except sqlite3.Error as e:

        print(e)

    render_template('list.html', rows=rows)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)