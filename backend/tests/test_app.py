import os
import pytest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Question, Category

DATABASE_USERNAME = os.environ.get("TRIVIA_DB_USERNAME")
DATABASE_PASSWORD = os.environ.get("TRIVIA_DB_PASSWORD")
DATABASE_NAME = "trivia_app_test"
TEST_DATABASE_PATH = database_path=f"postgres://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@localhost:5432/{DATABASE_NAME}"


@pytest.fixture
def test_app():
    app = create_app()
    client = app.test_client()
    setup_db(app, TEST_DATABASE_PATH)
    return client


def test_ping(test_app):
    res = test_app.get("/ping")
    assert res.status_code == 200
    assert res.json == "pong"


def test_get_all_categories(test_app):
    res = test_app.get("/categories")
    assert res.status_code == 200
    assert len(res.json["categories"]) == 6
