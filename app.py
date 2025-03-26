from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLALchemy
from flask_jwt_extended import JWTManager, create_acces_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from models import db, user,Task
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL']="sqlite:////tasks.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION']= False
app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")
db.init_app(app)
jwt = JWTManager(app)

#enable cors for routes ,allowing request from https"//local host 5173
CORS(app, resources={r"/*":{"origin":"http://localhost:5173"}})

with app.app_context():
    db.create_all()

@app.route("/register", methods=["POST"]) 
def register():
    data = request.get_json() 
    if user.query.filter_by(usrname=data["username"]).first():
        return jsonify({"msg":"usrename already exists, choose another name!"}), 400
    user = user(username =data["username"], password=data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg":"Account created successfully"}),201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    if not user or user.password !=data["password"]:
        return jsonify({"msg":"invalid credential. either the username or password is wrong!" }),
    token = create_access_token(identity=user.id)
    return jsonify({"token": token}),401

@app.route("/tasks", methods=["POST"])
@jwt_required()
def add_task():
    user_id = get_jwt_identity()
    data = request.get.get_json()
    start_time = datetime.now() if data["start_now"] else datetime.strptime(data['start_time'],"%Y-%m-%dT%H:%M")
    task = Task(title=data["title"], start_time=start_time, duration=data["duration"], user_id=user_id)
    db.session.add(task)
    db.session.commit()
    return jsonify({"msg":"task added"}),201

@app.route("/tasks",methods=["GET"])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([{"id":t.id, "title":t.title, " start_time " ;t.start_time.isoformat(), "duration":t.duraction}for t in task])

if __name__=="__main__":
    app.run(debug=True, port=5000)