from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["JWT_SECRET_KEY"] = "your_secret_key"
db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# db.create_all()

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    new_user = User(username=data["username"], password=data["password"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message="User registered"), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"], password=data["password"]).first()
    if user:
        access_token = create_access_token(identity=data["username"])
        return jsonify(access_token=access_token)
    return jsonify(message="Invalid credentials"), 401

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify(message="Protected route accessed")

if __name__ == "__main__":
    app.run(debug=True)
