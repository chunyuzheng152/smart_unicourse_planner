smart_unicourse_planner


chunyuzheng 24279373
cameron wright 23508669
yupei zhou 24306764
course_selector_tool


Flask
Flask-WTF
Flask-SQLAlchemy
Flask-Migrate
pytest
selenium
Werkzeug

## Running Tests

This project uses `pytest` for unit tests and `selenium` for browser-based tests.

### 1. Install dependencies

First, make sure you are in the project root folder. Then run:

 
    pip install -r requirements.txt

    pytest -v # run all test

    pytest tests/test_routes.py -v


Test folder structure

The testing files are stored in the tests/ folder:

tests/
├── conftest.py
├── test_routes.py
├── test_security.py
└── test_selenium.py