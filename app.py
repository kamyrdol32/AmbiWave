import functools

from flask import Flask, render_template, session, redirect

app = Flask(__name__)



### DECORATOR ###

def protected(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "isLogged" not in session:
            return redirect("/login")
        if "user" not in session:
            return redirect("/login")
        if "ID" not in session:
            return redirect("/login")
        return func(*args, **kwargs)

    return secure_function

@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/')
@protected
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=70)
