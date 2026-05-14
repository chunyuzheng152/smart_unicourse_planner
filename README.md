# Smart UniCourse Planner

Smart UniCourse Planner is a lightweight Flask web application created for the Agile Web Development (CITS3403) Group Project.

## Description

Smart UniCourse Planner helps students explore different majors (Computer Science, Data Science, Software Engineering), submit a short survey, and post comments in a discussion board for each major to create interaction among like-minded students. The application demonstrates Flask fundamentals: routing, templates, forms, file uploads, authentication basics, and database migrations.

## Team Members 

- Chunyu Zheng; 24279373; chunyuzheng152
- Cameron Wright; 23508669; cameronwright62
- Yupei Zhou; 24306764; yupei3305-byte

## Getting Started

Environment Variables

This project requires a `.env` file in the project root.
MUST:
Create a .env file in the project root based on .env.example:

APP_SECRET_KEY=dev-secret-key-change-this
APP_DATABASE_URL=sqlite:///project/app.db

Create virtual environment

```
python3 -m venv venv
source venv/bin/activate
```

Install Dependencies

```
pip install -r requirements.txt
```

Run app

```
python -m project.app
```

## Running Test

Run all tests

```
pytest -v
```

Run individual tests

```
conftest.py
pytest tests/test_models.py -v
pytest tests/test_routes.py -v
pytest tests/test_selenium.py -v
```
