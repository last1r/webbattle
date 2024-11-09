from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os
import sqlite3

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rating.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(150), nullable=False)
    school = db.Column(db.String(150), nullable=False)
    additional_education = db.Column(db.String(150), nullable=False)
    date = db.Column(db.String(30), nullable=True)
    time = db.Column(db.Integer(), nullable=True)
    scores = db.Column(db.Integer(), nullable=True)
    total_scores = db.Column(db.Integer(), nullable=True)
    fine = db.Column(db.Integer(), nullable=True)
    place_in_the_season = db.Column(db.Integer(), nullable=False)
    place_general = db.Column(db.Integer(), nullable=False)
    rank = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f'<Item {self.name}>'

with app.app_context():
    db.create_all()

FILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance/rating.db')

@app.route('/')
def index():
    files = os.listdir(FILES_DIR)
    return render_template('index.html', files=files)

@app.route('/download/<filename>')
def download_file(filename):
    if filename not in os.listdir(FILES_DIR):
        return 'FILE not found', 404
    return send_from_directory(FILES_DIR, filename)

def result(filename):

    conn = sqlite3.connect(f'files/{filename}')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM item")
    database = cursor.fetchall()
    conn.close()

    conn1 = sqlite3.connect('instance/rating.db')
    cursor1 = conn1.cursor()

    for el in database:
        if el:
            cursor1.execute(f"UPDATE item SET time = {el[2]}, scores = {round((el[3] * el[4]) / el[5], 2)}, fine = {el[4]}, total_scores = {el[5]} WHERE id={el[0]}")

    conn1.commit()
    conn1.close()

@app.route('/upload', methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return 'No file', 400

    file = request.files['file']

    if file.filename == '':
        return 'No selected file', 400

    if file:
        file.save(os.path.join(FILES_DIR, file.filename))
        print(file, file.filename, type(file))
        result(file.filename)
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

