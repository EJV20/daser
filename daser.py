from flask import Flask, request, url_for, redirect, session, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app = Flask(__name__, template_folder="FrontEnd/render_templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'
db = SQLAlchemy(app)
app.config.update(dict(SEND_FILE_MAX_AGE_DEFAULT=0))


users = {}


class User(db.Model):
    name = db.Column(db.String(80), primary_key=True, unique=True)
    pas = db.Column(db.String(80))

    def __init__(self, nm, ps):
        self.name = nm
        self.pas = ps


# by default, direct to login
@app.route("/")
def default():
    return redirect(url_for("logger"))


@app.route("/login/", methods=["GET", "POST"])
def logger():
    login_error = "No Errors"
    # Load in user names and passwords
    load = User.query.all()
    users.clear()
    for b in load:
        users.update({b.name: b.pas})

    # first check if the user is already logged in
    if "username" in session and "username" in users:
        if session["username"] in users:
            return redirect(url_for("start", username=session["username"]))

    # if not, and the incoming request is via POST try to log them in
    elif request.method == "POST":
        if request.form["but"] == "Login":
            if request.form["user"] in users and users[request.form["user"]] == request.form["pass"]:
                session["username"] = request.form["user"]
                session_name = request.form["user"]
                return redirect(url_for("start", username=session_name))
            else:
                login_error = 'Incorrect Username or Password'
        elif request.form["but"] == "Sign Up":
            if request.form["nuser"] not in users:
                u5 = User(request.form["nuser"], request.form["npass"])
                db.session.add(u5)
                db.session.commit()

                session["username"] = request.form["nuser"]
                session_name = request.form["nuser"]
                return redirect(url_for("start", username=session_name))
            else:
                login_error = 'Name already taken'

    return render_template("login.html", error=login_error)


@app.route("/start")
def start():
    # Render base template
    return render_template("index.html", name=session['username'])


# initialize the database
@app.cli.command('initdb')
def initdb_command():
    """Reinitializes the database"""
    db.drop_all()
    db.create_all()

    u1 = User("Je", "Pass")
    u2 = User("Ni", "Pass")
    u3 = User("Ga", "Pass")
    u4 = User("Em", "Pass")

    db.session.add(u1)
    db.session.add(u2)
    db.session.add(u3)
    db.session.add(u4)

    # commit
    db.session.commit()
    print('Initialized the database.')


@app.route("/logout/")
def unlogger():
    # if logged in, log out, otherwise offer to log in
    if "username" in session:
        # note, here were calling the .clear() method for the python dictionary builtin
        session.clear()
        # flashes are stored in session["_flashes"], so we need to clear the session /before/ we set the flash message!
        flash("Successfully logged out!")
        # we got rid of logoutpage.html!
        return redirect(url_for("logger"))
    else:
        flash("Not currently logged in!")
        return redirect(url_for("logger"))


if __name__ == '__main__':
    app.run()

app.secret_key = 'LKDJFDKjfkdj;sd;ifh:ID;iJ::KLd'
