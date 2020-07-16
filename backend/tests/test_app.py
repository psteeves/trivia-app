import os
import pytest
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

from app import create_app
from models import Question, Category, db

DATABASE_USERNAME = os.environ.get("TRIVIA_DB_USERNAME")
DATABASE_PASSWORD = os.environ.get("TRIVIA_DB_PASSWORD")
DATABASE_NAME = "trivia_app_test"
TEST_DATABASE_PATH = database_path=f"postgres://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@localhost:5432/{DATABASE_NAME}"


@pytest.fixture
def test_app():
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.drop_all()
    db.create_all()

    client = app.test_client()

    first_question = Question(question="Is there anybody out there?", answer="No", category="2", difficulty=5)
    second_question = Question(question="Mother do you think they'll drop the bomb?", answer="Yes", category="2", difficulty=5)

    first_question.insert()
    second_question.insert()

    yield client
    first_question.delete()
    second_question.delete()


def test_ping(test_app):
    res = test_app.get("/ping")
    assert res.status_code == 200
    assert res.json == "pong"


def test_get_all_questions(test_app):
    res = test_app.get("/questions")
    assert res.status_code == 200
    assert len(res.json["questions"]) == 2


def test_delete_question(test_app):
    # Make sure we start with two questions
    res = test_app.get("/questions")
    assert len(res.json["questions"]) == 2

    # Delete question
    res = test_app.delete("/questions/1")
    assert res.status_code == 200
    assert res.json == 1

    # Make sure question was deleted
    res = test_app.get("/questions")
    assert len(res.json["questions"]) == 1


def test_add_question(test_app):
    # Make sure we start with two questions
    res = test_app.get("/questions")
    assert len(res.json["questions"]) == 2

    # Add question
    res = test_app.post("/questions", json={"question": "New!", "answer":"Wow!", "category":"1", "difficulty":1})
    assert res.status_code == 200
    assert res.json == 3

    # Make sure question was added
    res = test_app.get("/questions")
    assert len(res.json["questions"]) == 3
