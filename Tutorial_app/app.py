from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

db = SQLAlchemy(app)


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return jsonify({
        "message": "Flask API running"
    })

@app.route("/users", methods=["POST"])
def create_user():

    data = request.get_json()

    user = User(
        name=data["name"],
        age=data["age"]
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "User created"
    })

@app.route("/users", methods=["GET"])
def get_users():

    users = User.query.all()

    output = []

    for user in users:
        output.append({
            "id": user.id,
            "name": user.name,
            "age": user.age
        })

    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)