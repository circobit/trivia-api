from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)

    CORS(app)

    with app.app_context():
        db.create_all()

    @app.after_request
    def after_request(response):
        # Allow any origina to access
        response.headers.add("Access-Control-Allow-Origin", "*")
        # Allow specific headers
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
        # Allow specific HTTP methods
        response.headers.add("Access-Control-Allow-Methods", "GET,POST,PATCH,DELETE,OPTIONS")

        return response


    # Questions endpoint
    @app.route('/questions', methods=['GET'])
    def get_questions():
        #Get all questions and categories.
        total_questions = Question.query.count()
        categories_objects = Category.query.all()
        categories = { category.id: category.type for category in categories_objects }

        page_str = request.args.get("page", '1')
        # Validate input and calculate offset
        try:
            # Attempt conversion to catch non-numeric strings
            page = int(page_str)
            # Check for invalid integer values
            if page <= 0:
                abort(422)
            # Calculate offset (the number of items to skip)
            offset = (page - 1) * QUESTIONS_PER_PAGE

        except ValueError:
            abort(422)
        
        # Pagination query
        question_query = Question.query.order_by(Question.id)
        # Apply limit of 10 and the calculated offset
        questions_on_page = question_query.limit(QUESTIONS_PER_PAGE).offset(offset).all()

        # Handle out of range page
        if not questions_on_page:
            abort(404)

        # Format questions
        formatted_questions = [ question.format() for question in questions_on_page ]

        # Return response
        return jsonify({
            "success": True,
            "questions": formatted_questions,
            "total_questions": total_questions,
            "categories": categories,
            "current_category": "All"
        }), 200


    # Categories endpoint
    @app.route("/categories", methods=["GET"])
    def get_categories():
        # Get categories
        categories_objects = Category.query.all()
        categories = { category.id: category.type for category in categories_objects }

        if not categories:
            abort(404)
        else:
            return jsonify({
                "success": True,
                "categories": categories
            }), 200


    # Delete questions endpoint
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        # Get question by ID
        question = db.session.get(Question, question_id)

        # Check if question exists
        if question is None:
            abort(404)
        else:
            # Delete question
            question.delete()

            return jsonify({
                "success": True
            }), 200


    @app.route("/questions", methods=["POST"])
    def create_question():
        # Get body
        body = request.get_json()
        # Get the values from the body
        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_category = body.get("category", None)
        new_difficulty = body.get("difficulty", None)
        # Check if any required fields are missing
        if not all([new_question, new_answer, new_category, new_difficulty]):
            abort(422)
        # Catch the bad data type and return 400.
        # Explicitly validate that 'difficulty' and 'category' are integers.
        # This is a preventative measure. The database is strict about its Integer
        # columns and will throw a fatal error if it receives a non-numeric string
        # (e.g., "three").
        try:
            int(new_difficulty)
            int(new_category)
        except (ValueError, TypeError):
            abort(400)
        try:
            # Create a new Question instance
            question = Question(
                question=new_question,
                answer=new_answer,
                category=new_category,
                difficulty=new_difficulty
            )
            # Add new question
            question.insert()
            # Return successful response
            return jsonify({
                "success": True,
                "created": question.id,
                "total_questions": Question.query.count()
            }), 201
        except Exception as e:
            db.session.rollback()
            abort(422)
    
        abort(422)


    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        # Get body
        body = request.get_json()
        # Get the values from the body
        search_term = body.get("searchTerm", None)

        # Check if search term is None
        if search_term is None:
            abort(400)
        
        # Search results
        search_results = Question.query.filter(
            Question.question.ilike(f"%{search_term}%")
        ).all()

        # Format questions
        formatted_questions = [ question.format() for question in search_results ]

        return jsonify({
            "success": True,
            "questions": formatted_questions,
            "total_questions": len(search_results),
            "current_category": None
        }), 200


    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify ({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify ({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify ({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify ({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422


    return app

