from datetime import datetime

from flask import Flask, request, url_for, redirect, session, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="FrontEnd/render_templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'
db = SQLAlchemy(app)
app.config.update(dict(SEND_FILE_MAX_AGE_DEFAULT=0))

users = {}


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column('post_id', db.Integer, primary_key=True, unique=True)
    text = db.Column('post_text', db.String(300))
    time = db.Column('post_time', db.String(20))
    user_name = db.Column(db.String(80), db.ForeignKey('users.user_name'))
    user = db.relationship('User')

    def __init__(self, txt, usr, tm):
        self.text = txt
        self.user_name = usr
        self.time = tm


class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id', db.Integer, primary_key=True, unique=True)
    name = db.Column('user_name', db.String(80), unique=True)
    pas = db.Column('user_pw', db.String(80))
    date = db.Column('created_date', db.String(20))

    def __init__(self, nm, ps, tm):
        self.name = nm
        self.pas = ps
        self.created = tm


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
            return redirect(url_for("feed", username=session["username"]))

    # if not, and the incoming request is via POST try to log them in
    elif request.method == "POST":
        if request.form["but"] == "Login":
            if request.form["user"] in users and users[request.form["user"]] == request.form["pass"]:
                session["username"] = request.form["user"]
                session_name = request.form["user"]
                return redirect(url_for("feed", username=session_name))
            else:
                login_error = 'Incorrect Username or Password'
        elif request.form["but"] == "Sign Up":
            if request.form["nuser"] not in users:
                u5 = User(request.form["nuser"], request.form["npass"], datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                db.session.add(u5)
                db.session.commit()

                session["username"] = request.form["nuser"]
                session_name = request.form["nuser"]
                return redirect(url_for("feed", username=session_name))
            else:
                login_error = 'Name already taken'

    return render_template('login.html', error=login_error)


@app.route("/feed")
def feed():
    # Query for feed
    f = Post.query.limit(10)
    m = Post.query.filter_by(user_name=session['username']).limit(10)

    if request.method == "POST":
        if request.form["but"] == "Feed":
            redirect(url_for('feed'))
        elif request.form["but"] == "Profile":
            redirect(url_for('profile'))
        elif request.form["but"] == "Leaders":
            redirect(url_for('leaders'))

    return render_template("feed.html", name=session['username'], feeds=f,
                           meeds=m)


@app.route("/profile")
def message():
    return render_template("profile.html")


@app.route("/leaders")
def leaders():
    return render_template("leaders.html")


# initialize the database
@app.cli.command('initdb')
def initdb_command():
    """Reinitializes the database"""
    db.drop_all()
    db.create_all()

    u1 = User("Je", "Pass", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    u2 = User("Ni", "Pass", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    u3 = User("Ga", "Pass", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    u4 = User("Em", "Pass", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    p1 = Post("Hello World", "Je", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    p2 = Post("Hello World - Nick", "Ni", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    p3 = Post("Hello World - Gabe", "Ga", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    p4 = Post("Hello World - Emily", "Em", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    db.session.add(u1)
    db.session.add(u2)
    db.session.add(u3)
    db.session.add(u4)
    db.session.add(p1)
    db.session.add(p2)
    db.session.add(p3)
    db.session.add(p4)
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
