from functions import *

import functools

from flaskext.mysql import MySQL
from flask_mail import Mail
from flask import Flask, render_template, session, redirect, request, flash, jsonify
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
            flash("Ta zawartość wymaga posiadania konta na stronie", "error")
            return redirect("/")
        if "user" not in session:
            flash("Ta zawartość wymaga posiadania konta na stronie", "error")
            return redirect("/")
        if "ID" not in session:
            flash("Ta zawartość wymaga posiadania konta na stronie", "error")
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
            session['username'] = getUsername(login_email)
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
            flash("Hasła muszą byc identyczne!", "error")
            return redirect("/")

        # Development
        if Type == "Development":
            print("Rejestracja userName: " + register_username)
            print("Rejestracja E-mail: " + register_email)
            print("Rejestracja Hasło: " + register_password)
            print("Rejestracja Hasło: " + register_password_2)

        if userRegister(register_username, register_email, register_password):

            flash("Konto zostało stworzone, na podany adres E-mail został wysłany kod aktywacyjny", "success")

            return redirect("/")

        else:

            flash("Podany E-Mail jest juz zarejestrowany!", "error")
            return redirect("/")

    return render_template("index.html")

@app.route('/activate/<int:ID>/<string:KEY>', methods=['POST', 'GET'])
def activate(ID, KEY):

    # Development
    if Type == "Development":
        print("Activate ID: " + str(ID))
        print("Activate KEY: " + str(KEY))

    if userActivate(ID, KEY):
        flash("Konto zostało pomyślnie aktywowane!", "success")
    else:
        flash("Nastąpił błąd podczas aktywacji!", "error")

    return redirect("/")

@app.route('/logout')
@protected
def logout():
    session.pop('isLogged', None)
    session.pop('user', None)
    session.pop('username', None)
    session.pop('ID', None)
    return redirect("/")

####################
### HOME ###
####################

@app.route('/home', methods=['POST', 'GET'])
@protected
def home():

    SongsList = getSongsList()
    FavoriteList = getFavoritesSongsList(session["ID"])

    print(SongsList)
    print(FavoriteList)

    return render_template("home.html", SongsList=SongsList, FavoriteList=FavoriteList)

@app.route('/song/<int:ID>')
@protected
def song(ID):

    print(ID)

    return render_template("song.html")

@app.route('/favorite', methods=['POST', 'GET'])
@app.route('/favorite/<token>', methods=['POST', 'GET'])
@protected
def favorite(token=False):

    Songs = []

    # Własna playlista
    if not token:

        FavoritesSongs = getFavoritesSongsList(session["ID"])
        for Data in FavoritesSongs:
            Songs.append(getSongInfo(Data))

    # Kogos playlista
    else:

        ID = getUserIDbyToken(token)

        FavoritesSongs = getFavoritesSongsList(ID)
        for Data in FavoritesSongs:
            Songs.append(getSongInfo(Data))

    return render_template("favorite.html", SongsList=Songs)

@app.route('/favorite/add')
@protected
def favorite_add():
    SongID = request.args.get('id', 0, type=int)

    # Development
    if Type == "Development":
        print("Favorite: " + str(SongID))

    addToFavorite(session["ID"], SongID)

    return jsonify(SongID)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=70)
