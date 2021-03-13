import functools

from flaskext.mysql import MySQL
from flask import Flask, render_template, session, redirect, request

####################
### CONFIG & DECORATOS
####################

Type = "Development" # Production or Development

# Pobieranie config'a z pliku config.py
app = Flask(__name__)
app.config.from_object("config." + Type + "Config")

# Aktywowanie modułu MySQL & Mail
mysql = MySQL()

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
    if request.method == "POST":
        login_mail = request.form.get('login_mail', "", type=str)
        login_password = request.form.get('login_password', "", type=str)
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=70)
