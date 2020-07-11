from flask import Flask, render_template, request, session, escape
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

import os
dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/DBs/database.db"

app = Flask(__name__) 
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80))

def seccion():
    try:
        # sess=escape(session["username"]).upper()
        sess = {}
        sess["username"] = session["username"]
        sess["email"] = session["email"]
    except Exception as e:
        print("TypeError: {} - Error: {}".format(type(e),e))
        # sess["username"] = "NONE"
        sess = "NONE"
    return sess

@app.route("/")
def index():
    users = Users.query.all()
    user_list = users
    return render_template("index.html", dbdir=dbdir, user_list=user_list, session=seccion())

@app.route("/search")
def search():
    nickname = request.args.get("nickname")
    user = Users.query.filter_by(username=nickname).first()
    if user:
        return render_template("msg.html", msg=str(user.id)+" - "+(user.username)+" - "+(user.email), session=seccion())
    return render_template("msg.html", msg="The user doesn't exist.", session=seccion())

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        hashed_pw = generate_password_hash(request.form["password"], method="sha256")
        new_user = Users(   username=request.form["username"], 
                            password=hashed_pw, 
                            email=request.form["email"]   )
        db.session.add(new_user)
        db.session.commit()

        # return "You've registered successfully."
        return render_template("msg.html", msg="You've registered successfully.", session=seccion())

    return render_template("signup.html", session=seccion())

@app.route("/login", methods=["GET", "POST"])
def login():
    # POST
    if request.method == "POST":
        user = Users.query.filter_by(username=request.form["username"]).first()

        if user and check_password_hash(user.password, request.form["password"]):
            session["username"] = user.username
            session["email"] = user.email
            # return "You are logged in"
            return render_template("msg.html", msg="You are logged in", session=seccion())
        # return "Your credentials are invalid, check and try again."
        return render_template("msg.html", msg="Your credentials are invalid, check and try again.", session=seccion())

    # GET
    return render_template("login.html", session=seccion())

@app.route("/home")
def home():
    if "username" in session:
        # return "You are %s" % seccion()
        return render_template("msg.html", msg="You are %s" % seccion(), session=seccion())

    # return "You must log in first."
    return render_template("msg.html", msg="You must log in first.", session=seccion())

@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("email", None)
    # return "You are logged out."
    return render_template("msg.html", msg="You are logged out.", session=seccion())

app.secret_key = "12345"


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=5001)
