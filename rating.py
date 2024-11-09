from operator import itemgetter

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.secret_key = b'_5!!@#y2L"F4Q8@z\n\xec]/awwgwfd2w@@'

# app.config['SECRET_KEY'] = '_5!!@#y2L"F4Q8@z\n\xec]/awwgwfd2w@@'
# bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rating.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class reginfo(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    mail = db.Column(db.String(), nullable=True)
    phone = db.Column(db.String(), nullable=True)
    city = db.Column(db.String(150), nullable=False)
    school = db.Column(db.String(150), nullable=False)
    additional_education = db.Column(db.String(150), nullable=False)

class rating(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    scores = db.Column(db.Integer(), nullable=True)

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return reginfo.query.get(int(user_id))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        if request.method == "POST":
            name = request.form["name"]
            password = request.form["password"]

            user = reginfo.query.filter_by(name=name).first()
            data = reginfo.query.filter_by(name=name, password=password).first()
            if data is not None:
            # if user and bcrypt.check_password_hash(user.password, password):
                login_user(user)
                session['login_in'] = True
                return redirect(url_for("rating_one"))
        return render_template("login.html")
    except:
        return render_template("error.html")

@app.route("/register", methods=["GET", "POST"])
def reg():
    try:
        if request.method == "POST":
            name = request.form['name']
            mail = request.form['mail']
            password = request.form['password']
            phone = request.form['phone']
            city = request.form['city']
            school = request.form['school']
            additional_education = request.form['additional_education']

            register = reginfo(name=name, mail=mail, password=password, phone=phone, city=city, school=school, additional_education=additional_education)
            db.session.add(register)
            db.session.commit()

            return redirect(url_for("login"))
        return render_template("register.html")
    except:
        return render_template("error.html")

@app.route("/rating_one", methods=["GET", "POST"])
@login_required
def rating_one():
    try:
        if not session.get('login_in'):
            return render_template("index.html")
        if session.get('login_in'):
            if request.method == "POST":
                one = request.form['one']
                rating_tabl = rating(name=current_user.name, scores=sum(int(i) for i in one)*0.5)
                db.session.add(rating_tabl)
                db.session.commit()
    
                return render_template('index.html')
            return render_template('rating_one.html')
    except:
        return render_template("error.html")

@app.route("/rating")
def rating_tab():
    try:
        return render_template('rating.html', items=sorted([[i.name, i.scores] for i in rating.query.all()], key=lambda x: x[1])[::-1])
    except:
        return render_template("error.html")

@app.route("/logout")
@login_required
def logout():
    session['login_in'] = False
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)