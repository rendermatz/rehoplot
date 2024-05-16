import sqlite3
from flask import Flask, render_template, request,app
from datetime import *

app= Flask(__name__, template_folder="templates")





if __name__ == '__main__':
    app.run(host="0.0.0.0", port='5000')