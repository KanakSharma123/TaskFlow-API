import json
from flask import Flask
from dotenv import load_dotenv
import os
from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException
from marshmallow import ValidationError
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from datetime import timedelta
from models import db, User, Task, Project
from schemas import (
    UserSchema,
    ProjectSchema,
    TaskSchema
)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
app = Flask(__name__)
SWAGGER_URL = "/docs"

API_URL = "/swagger.json"


swaggerui_blueprint = get_swaggerui_blueprint(

    SWAGGER_URL,

    API_URL,

    config={
        "app_name":"TaskFlow API"
    }

)


app.register_blueprint(
    swaggerui_blueprint,
    url_prefix=SWAGGER_URL
)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=5)
print("DB URL:", os.getenv("SQLALCHEMY_DATABASE_URI"))
print("JWT:", os.getenv("JWT_SECRET_KEY"))
db.init_app(app)

jwt = JWTManager(app)
@app.errorhandler(HTTPException)
def handle_http_error(error):

    return jsonify({

        "error": error.name,
        "message": error.description

    }), error.code



@app.errorhandler(Exception)
def handle_general_error(error):

    return jsonify({

        "error": "Internal Server Error",
        "message": str(error)

    }), 500

user_schema = UserSchema()

project_schema = ProjectSchema()

task_schema = TaskSchema()

@app.route("/")
def home():

    return {
        "message":"TaskFlow API running"
    }



@app.route("/register", methods=["POST"])
def register():

    try:

        data = user_schema.load(
            request.json
        )

    except ValidationError as err:

        return {
            "error":err.messages
        },400

    user=User(
        username=data["username"],
        password=data["password"]
    )

    db.session.add(user)
    db.session.commit()

    return {
        "message":"User created"
    }



@app.route("/login", methods=["POST"])
def login():

    data=request.json

    user=User.query.filter_by(
        username=data["username"]
    ).first()


    if user and user.password==data["password"]:

        token=create_access_token(
            identity=str(user.id)
        )

        return {
            "token":token
        }


    return {
        "error":"Invalid credentials"
    },401



@app.route("/tasks", methods=["POST"])
@jwt_required()
def create_task():

    data = request.json


    task = Task(
        title=data["title"],
        priority=data.get("priority","Medium"),
        project_id=data["project_id"]
    )


    db.session.add(task)
    db.session.commit()


    return {
        "message":"Task created"
    }




@app.route("/tasks",methods=["GET"])
@jwt_required()
def get_tasks():

    user_id=get_jwt_identity()


    tasks=Task.query.filter_by(
        user_id=user_id
    ).all()


    result=[]


    for t in tasks:

        result.append({

            "id":t.id,
            "title":t.title,
            "status":t.status,
            "priority":t.priority

        })


    return jsonify(result)




@app.route("/tasks/<int:id>",methods=["PUT"])
@jwt_required()
def update_task(id):

    task=Task.query.get(id)

    try:

        data = task_schema.load(
            request.json
        )


    except ValidationError as err:

        return {
            "error":err.messages
        },400


    task.status=data["status"]

    db.session.commit()


    return {
        "message":"Updated"
    }



@app.route("/tasks/<int:id>",methods=["DELETE"])
@jwt_required()
def delete_task(id):

    task=Task.query.get(id)

    db.session.delete(task)

    db.session.commit()


    return {
        "message":"Deleted"
    }

@app.route("/projects", methods=["POST"])
@jwt_required()
def create_project():

    user_id = get_jwt_identity()

    try:

        data = project_schema.load(
            request.json
        )


    except ValidationError as err:

        return {
            "error":err.messages
        },400


    project = Project(
        name=data["name"],
        user_id=user_id
    )


    db.session.add(project)
    db.session.commit()


    return {
        "message":"Project created"
    }




@app.route("/projects", methods=["GET"])
@jwt_required()
def get_projects():

    user_id = get_jwt_identity()


    projects = Project.query.filter_by(
        user_id=user_id
    ).all()


    result=[]


    for p in projects:

        result.append({

            "id":p.id,
            "name":p.name

        })


    return jsonify(result)

@app.route("/projects/<int:project_id>/tasks", methods=["GET"])
@jwt_required()
def project_tasks(project_id):


    tasks = Task.query.filter_by(
        project_id=project_id
    ).all()


    result=[]


    for t in tasks:

        result.append({

            "id":t.id,
            "title":t.title,
            "status":t.status,
            "priority":t.priority

        })


    return jsonify(result)
@app.route("/swagger.json")
def swagger():

    with open("swagger.json") as f:

        return jsonify(json.load(f))

if __name__=="__main__":

    with app.app_context():

        db.create_all()


    app.run(debug=True)