import sqlite3
from flask import Flask, render_template, request


app=Flask(__name__)


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