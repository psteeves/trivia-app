import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from models import db, setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, supports_credentials=True)

    @app.route("/ping")
    def index():
        return jsonify("pong")

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response

    @app.route("/categories")
    def get_categories():
        categories = db.session.query(Category).order_by(Category.id).all()
        return jsonify({"categories": [category.format() for category in categories]})

    @app.route("/questions", methods=["GET", "POST"])
    def get_or_create_questions():
        if request.method == "GET":
            page = int(request.args.get("page", 1))
            start = (page -1) * QUESTIONS_PER_PAGE
            end = page * QUESTIONS_PER_PAGE
            search_term = request.args.get("query")

            db_query = db.session.query(Question)
            if search_term is not None:
                db_query = db_query.filter(Question.question.contains(search_term))
            questions = db_query.order_by(Question.id).all()

            return jsonify({"questions": [question.format() for question in questions][start:end], "total_questions": len(questions)})
        else:
            question_body = request.get_json()
            new_question = Question(question=question_body["question"], answer=question_body["answer"], category=question_body["category"], difficulty=question_body["difficulty"])
            new_question.insert()
            return jsonify(new_question.id)

    @app.route("/categories/<category_id>/questions")
    def get_questions_by_category(category_id):
        questions = db.session.query(Question).filter(Question.category == category_id).all()
        return jsonify({"questions": [question.format() for question in questions], "total_questions": len(questions)})

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        question = db.session.query(Question).filter(Question.id == question_id).one_or_none()
        if question is None:
            abort(404)

        question.delete()
        return jsonify(question.id)

    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
  
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''



    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
  
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

    return app
