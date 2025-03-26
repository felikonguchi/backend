from flask_sqlalchemy import SQLALalchemy

db = SQLALchemy()

class user(db.model):
    id = db.column(db.Integer, primary_key=True)
    username = db.column(db.string(80), unique=true, nullable=False)
    password = db.column(db.string(120),nullable=False)
    task = db.relationship("Task",backref=)
class Task(db.model):
    id= db.column(db.Integer,primary_key=True)
    title = db.column(db.string(225), nullable=False)
    start_time = db.column(db.DateTime,nullable=False)
    duration = db.column(db.Integer, nullable=False)
    user_id = db.column(db.integer,db.foreignkey("user.id"), nullable=False)    

