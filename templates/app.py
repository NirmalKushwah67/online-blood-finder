import _sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os


app = Flask(__name__)
app.secret_key = "mysecretkey"

# Database Config
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "blood.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# --------------------------------------------------------------------
# MODELS
# --------------------------------------------------------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))


class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    blood_group = db.Column(db.String(10))
    city = db.Column(db.String(100))
    phone = db.Column(db.String(15))

# --------------------------------------------------------------------
# ROUTES
# --------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")

# ----------------------- REGISTER -----------------------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")

        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        flash("Registration successful, please login!", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# ----------------------- LOGIN -----------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('blood.db')
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )
        user = cur.fetchone()
        conn.close()

        if user:
            return redirect('/')
        else:
            error = "Invalid email or password!"

    return render_template('login.html', error=error)


# ----------------------- LOGOUT -----------------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# ----------------------- DASHBOARD -----------------------

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")

# ----------------------- ADD DONOR -----------------------

@app.route("/add_donor", methods=["GET", "POST"])
def add_donor():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        donor = Donor(
            name=request.form["name"],
            age=request.form["age"],
            blood_group=request.form["blood_group"],
            city=request.form["city"],
            phone=request.form["phone"],
        )
        db.session.add(donor)
        db.session.commit()

        flash("Donor added successfully!", "success")
        return redirect(url_for("donors"))

    return render_template("add_donor.html")

# ----------------------- SHOW DONORS -----------------------

@app.route("/donors")
def donors():
    all_donors = Donor.query.all()
    return render_template("donors.html", donors=all_donors)

# ----------------------- FIND DONOR -----------------------

@app.route("/find", methods=["GET", "POST"])
def find():
    donors = []
    if request.method == "POST":
        blood_group = request.form["blood_group"]
        city = request.form["city"]

        donors = Donor.query.filter_by(blood_group=blood_group, city=city).all()

    return render_template("find.html", donors=donors)

# --------------------------------------------------------------------
# RUN APP
# --------------------------------------------------------------------

if __name__ == "__main__":
    with app.app_context():   # FIXED ERROR HERE
        db.create_all()

    app.run(debug=True)
