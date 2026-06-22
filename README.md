# TaskFlow - Task Management REST API

A backend task management system built using Flask with JWT authentication, database relationships, validation, error handling, and Swagger API documentation.

## Features

- User authentication using JWT
- Create and manage projects
- Create tasks under projects
- CRUD operations
- Input validation
- Global error handling
- Swagger API documentation
- SQLite database integration


## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- Flask-JWT-Extended
- Marshmallow
- Swagger UI


## Project Architecture
User --> Projects --> Tasks



## API Endpoints

### Authentication

POST `/register`

Create new user


POST `/login`

Generate JWT token


### Projects

POST `/projects`

Create project


GET `/projects`

Get user projects


### Tasks

POST `/tasks`

Create task


GET `/projects/<id>/tasks`

Get project tasks



## Running Locally


Clone repository:
git clone <repository-url>


Install dependencies:
pip install -r requirements.txt


Run application:
python app.py


Swagger Documentation:
http://127.0.0.1:5000/docs



## Future Improvements

- PostgreSQL integration
- Docker deployment
- Refresh tokens
- Role-based authentication
- Cloud deployment