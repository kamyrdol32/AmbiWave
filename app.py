from functions import *

import functools

from flaskext.mysql import MySQL
from flask_mail import Mail
from flask import Flask, render_template, session, redirect, request, flash
from others import check

####################
### CONFIG & DECORATOS
####################

Type = "Development" # Production or Development

# Pobieranie config'a z pliku config.py
app = Flask(__name__)
app.config.from_object("config." + Type + "Config")

# Aktywowanie modułu MySQL & Mail
mysql = MySQL()
mysql.init_app(app)
mail = Mail(app)

####################
### DECORATOR ###
####################

def protected(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "isLogged" not in session:
            return redirect("/")
        if "user" not in session:
            return redirect("/")
        if "ID" not in session:
            return redirect("/")
        return func(*args, **kwargs)

    return secure_function

@app.route('/', methods=['POST', 'GET'])
def index():

    # Logowanie
    if request.method == "POST" and request.form.get('action', "", type=str) == "Login":

        login_email = request.form.get('login_email', "", type=str)
        login_password = request.form.get('login_password', "", type=str)


        # if not check("Mail", login_email):
        #     return flash("Prosze wprowadzić poprawny adres E-Mail!")

        # Development
        if Type == "Development":
            print("Logowanie Login: " + login_email)
            print("Logowanie Hasło: " + login_password)

        if userLogin(login_email, login_password):

            session['isLogged'] = True
            session['user'] = login_email
            session['ID'] = getUserID(login_email)

            return redirect("/home")

        else:

            flash("Podane konto nie istnieje w naszej bazie danych!", "error")
            return redirect("/")

    # Rejestracja
    if request.method == "POST" and request.form.get('action', "", type=str) == "Register":

        register_username = request.form.get('register_username', "", type=str)
        register_email = request.form.get('register_email', "", type=str)
        register_password = request.form.get('register_password', "", type=str)
        register_password_2 = request.form.get('register_password_2', "", type=str)

        # Weryfikacja danych
        if not register_password == register_password_2:
            flash("Hasła nie są zgodne!")

        # Development
        if Type == "Development":
            print("Rejestracja userName: " + register_username)
            print("Rejestracja E-mail: " + register_email)
            print("Rejestracja Hasło: " + register_password)
            print("Rejestracja Hasło: " + register_password_2)

        if userRegister(register_username, register_email, register_password):

            session['isLogged'] = True
            session['user'] = register_email
            session['ID'] = getUserID(register_email)

            return redirect("/home")

        else:

            flash("Podany E-Mail !")
            return redirect("/")

    return render_template("index.html")

@app.route('/activate/<int:ID>/<string:KEY>', methods=['POST', 'GET'])
def activate(ID, KEY):

    # Development
    if Type == "Development":
        print("Activate ID: " + str(ID))
        print("Activate KEY: " + str(KEY))

    userActivate(ID, KEY)

    return redirect("/")

####################
### HOME ###
####################

@app.route('/home', methods=['POST', 'GET'])
def home():

    SongsList = getSongsList()

    return render_template("home.html", SongsList=SongsList)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=70)
