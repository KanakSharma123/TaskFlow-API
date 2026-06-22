from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(100),
        nullable=False
    )


    projects = db.relationship(
        "Project",
        backref="owner"
    )



class Project(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )


    tasks = db.relationship(
        "Task",
        backref="project"
    )



class Task(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Todo"
    )

    priority = db.Column(
        db.String(20),
        default="Medium"
    )


    project_id = db.Column(
        db.Integer,
        db.ForeignKey("project.id")
    )