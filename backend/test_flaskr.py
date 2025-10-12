import os
import unittest
import json

from flaskr import create_app
from models import db, Question, Category
from test_data import categories_data, questions_data
from unittest.mock import patch


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "trivia_test"
        self.database_user = "cristiancevasco"
        self.database_password = ""
        self.database_host = "localhost:5432"
        self.database_path = f"postgresql://{self.database_user}:{self.database_password}@{self.database_host}/{self.database_name}"

        # Create app with the test configuration
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True
        })
        self.client = self.app.test_client()

        # Bind the app to the current context and create all tables
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        
            # Create categories in database
            for data in categories_data:
                category_to_add = Category(type = data['type'])
                category_to_add.id = data['id']
                category_to_add.insert()
            # Create questions in database
            for data in questions_data:
                question_to_add = Question(
                    question=data['question'],
                    answer = data['answer'],
                    category = data['category_id'],
                    difficulty = data['difficulty']
                    )
                question_to_add.insert()


    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    # Tests for /questions endpoint
    def test_get_paginated_questions(self):
        # Get response object
        res = self.client.get("/questions?page=1")
        # Extract the data from the response in JSON format
        data = json.loads(res.data)
        
        # Check status code
        self.assertEqual(res.status_code, 200)
        # Check for expected fields in the response
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['current_category'])
        # Check if 'category' is a dict
        self.assertIsInstance(data['categories'], dict)
        # Check pagination rule (10 items per page)
        self.assertEqual(len(data['questions']), 10)


    def test_404_requesting_non_existent_page(self):
        # Get response object
        res = self.client.get("/questions?page=1000")
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Check status code
        self.assertEqual(res.status_code, 404)
        # Check for expected fields in the response
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")


    def test_422_if_page_parameter_is_not_positive(self):
        # Get response object for page=0
        res_zero = self.client.get("/questions?page=0")
        data_zero = json.loads(res_zero.data)

        # Check status code and response for page=0
        self.assertEqual(res_zero.status_code, 422)
        self.assertEqual(data_zero["success"], False)
        self.assertEqual(data_zero["message"], "unprocessable")

        # Get response object for page=-1
        res_negative = self.client.get("/questions?page=-1")
        data_negative = json.loads(res_negative.data)

        # Check status code and response for page=-1
        self.assertEqual(res_negative.status_code, 422)
        self.assertEqual(data_negative["success"], False)
        self.assertEqual(data_negative["message"], "unprocessable")


    def test_422_if_page_parameter_is_not_an_integer(self):
        # Get response object
        res = self.client.get("/questions?page=two")
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Check status code
        self.assertEqual(res.status_code, 422)
        # Check for expected fields in the response
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 422)
        self.assertEqual(data["message"], "unprocessable")
    

    def test_patch_method_not_allowed_questions(self):
        # Get response object
        res = self.client.patch("/questions")
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Check status code
        self.assertEqual(res.status_code, 405)
        # Check for expected fields in the response
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 405)
        self.assertEqual(data["message"], "method not allowed")
    

    def test_put_method_not_allowed_questions(self):
        # Get response object
        res = self.client.put("/questions")
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Check status code
        self.assertEqual(res.status_code, 405)
        # Check for expected fields in the response
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 405)
        self.assertEqual(data["message"], "method not allowed")
    

    def test_delete_method_not_allowed_questions(self):
        # Get response object
        res = self.client.delete("/questions")
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Check status code
        self.assertEqual(res.status_code, 405)
        # Check for expected fields in the response
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 405)
        self.assertEqual(data["message"], "method not allowed")


    # Tests for /categories endpoint
    def test_get_categories(self):
        # Get response object
        res = self.client.get("/categories")
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Check status code
        self.assertEqual(res.status_code, 200)
        # Check for expected fields in the response
        self.assertEqual(data["success"], True)
        self.assertIsInstance(data['categories'], dict)
        self.assertEqual(len(data['categories']), 6)
    

    def test_patch_method_not_allowed_categories(self):
        # Get response object
        res = self.client.patch("/categories")
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Check status code
        self.assertEqual(res.status_code, 405)
        # Check for expected fields in the response
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 405)
        self.assertEqual(data["message"], "method not allowed")


    def test_post_method_not_allowed_categories(self):
        # Get response object
        res = self.client.post("/categories")
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Check status code
        self.assertEqual(res.status_code, 405)
        # Check for expected fields in the response
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 405)
        self.assertEqual(data["message"], "method not allowed")
    

    def test_put_method_not_allowed_categories(self):
        # Get response object
        res = self.client.put("/categories")
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Check status code
        self.assertEqual(res.status_code, 405)
        # Check for expected fields in the response
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 405)
        self.assertEqual(data["message"], "method not allowed")
    

    def test_delete_method_not_allowed_categories(self):
        # Get response object
        res = self.client.delete("/categories")
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Check status code
        self.assertEqual(res.status_code, 405)
        # Check for expected fields in the response
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 405)
        self.assertEqual(data["message"], "method not allowed")
    

    # Test for question deletion by id -> /questions/<id>
    def test_delete_question_by_id(self):
        # Get response object
        res = self.client.delete(f"/questions/5")
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Check status code
        self.assertEqual(res.status_code, 200)
        # Check for expected fields in the response
        self.assertEqual(data["success"], True)
        # FIX: Wrap the database check inside the application context
        with self.app.app_context():
            # Make sure the object was deleted
            question = db.session.get(Question, 5)
            self.assertIsNone(question)
    

    def test_404_delete_non_existent_question(self):
        # Get response object
        res = self.client.delete(f"/questions/1000")
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Check status code
        self.assertEqual(res.status_code, 404)
        # Check for expected fields in the response
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")
    

    def test_405_get_on_delete_route(self):
        # Get response object
        res = self.client.get(f"/questions/7")
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Check status code
        self.assertEqual(res.status_code, 405)
        # Check for expected fields in the response
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 405)
        self.assertEqual(data["message"], "method not allowed")
    

    def test_405_patch_on_delete_route(self):
        # Get response object
        res = self.client.patch(f"/questions/7")
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Check status code
        self.assertEqual(res.status_code, 405)
        # Check for expected fields in the response
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 405)
        self.assertEqual(data["message"], "method not allowed")
    

    def test_405_post_on_delete_route(self):
        # Get response object
        res = self.client.post(f"/questions/7")
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Check status code
        self.assertEqual(res.status_code, 405)
        # Check for expected fields in the response
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 405)
        self.assertEqual(data["message"], "method not allowed")
    

    def test_405_put_on_delete_route(self):
        # Get response object
        res = self.client.put(f"/questions/7")
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Check status code
        self.assertEqual(res.status_code, 405)
        # Check for expected fields in the response
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 405)
        self.assertEqual(data["message"], "method not allowed")
    

    # Tests for creations of questions in the /questions endpoint
    def test_create_new_question(self):
        # Use app context to call the db
        with self.app.app_context():
            # Get the number of total questions before the operations
            total_questions_before = Question.query.count()
        # Question to create
        question_to_add = {
            "question": "In which year did the Berlin Wall fall, leading to the reunification of Germany?",
            "answer": "1989",
            "category": 4,
            "difficulty": 2
        }
        # Get response object
        res = self.client.post(f"/questions", json=question_to_add)
        # Extract the data from the response in JSON format
        data = json.loads(res.data)
        # Use app context to call the db
        with self.app.app_context():
            # Get total questions after adding the question
            total_questions_after = Question.query.count()

        # Check status code
        self.assertEqual(res.status_code, 201)
        # Check for expected fields in the response
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        # Check that the total questions increased by 1
        self.assertEqual(total_questions_after, total_questions_before + 1)


    # Simulate an unexpected database error (for example, connection lost) 
    # and ensure the rollback logic is tested
    @patch('models.Question.insert')
    def test_422_if_question_insert_fails(self, mock_insert):
        # Configure the mock to raise a generic exception
        mock_insert.side_effect = Exception("Database error")

        # Question data that is otherwise valid
        question_to_add = {
            "question": "This question will fail to insert.",
            "answer": "Due to a mock error.",
            "category": 1,
            "difficulty": 1
        }
        
        # Make the request
        res = self.client.post("/questions", json=question_to_add)
        data = json.loads(res.data)

        # Assert that the request is unprocessable
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    

    def test_400_bad_request_create_question(self):
        # Use app context to call the db
        with self.app.app_context():
            # Get the number of total questions before the operations
            total_questions_before = Question.query.count()
        # Question to create
        question_to_add = {
            "question": "What is acrophobia a fear of?",
            "answer": "Heights",
            "category": 2,
            "difficulty": "three"
        }
        # Get response object
        res = self.client.post(f"/questions", json=question_to_add)
        # Extract the data from the response in JSON format
        data = json.loads(res.data)
        # Use app context to call the db
        with self.app.app_context():
            # Get total questions after adding the question
            total_questions_after = Question.query.count()
        # Check status code
        self.assertEqual(res.status_code, 400)
        # Check for expected fields in the response
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")
        # Check that the total number of questions wasn't increased
        self.assertEqual(total_questions_after, total_questions_before)
        

    def test_422_if_question_creation_fails(self):
        # Use app context to call the db
        with self.app.app_context():
            # Get the number of total questions before the operations
            total_questions_before = Question.query.count()
        # Question to create
        question_to_add = {
            "question": "Who was the Ancient Greek God of the Sun?",
            "category": 4,
            "difficulty": 2
        }
        # Get response object
        res = self.client.post(f"/questions", json=question_to_add)
        # Extract the data from the response in JSON format
        data = json.loads(res.data)
        # Use app context to call the db
        with self.app.app_context():
            # Get total questions after adding the question
            total_questions_after = Question.query.count()

        # Check status code
        self.assertEqual(res.status_code, 422)
        # Check for expected fields in the response
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
        # Check that the total number of questions wasn't increased
        self.assertEqual(total_questions_after, total_questions_before)
    

    # Test search questions
    def test_search_questions_with_results(self):
        # Payload to send
        search_data = {"searchTerm": "planet"}
        # Get response object
        res = self.client.post(f"/questions/search", json=search_data)
        # Extract the data from the response in JSON format
        data = json.loads(res.data)
        
        # Check status code
        self.assertEqual(res.status_code, 200)
        # Check for expected fields in the response
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["questions"]), 2)
        self.assertEqual(data["total_questions"], 2)
        # Check if content is correct
        for question in data["questions"]:
            self.assertIn("planet", question["question"].lower())
    

    def test_search_is_case_insensitive(self):
        # Payload to send
        search_data = {"searchTerm": "pLaNeT"}
        # Get response object
        res = self.client.post(f"/questions/search", json=search_data)
        # Extract the data from the response in JSON format
        data = json.loads(res.data)
        
        # Check status code
        self.assertEqual(res.status_code, 200)
        # Check for expected fields in the response
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["questions"]), 2)
        self.assertEqual(data["total_questions"], 2)
        # Check if content is correct
        for question in data["questions"]:
            self.assertIn("planet", question["question"].lower())
    

    def test_search_matches_substrings(self):
        # Payload to send
        search_data = {"searchTerm": "larg"}
        # Get response object
        res = self.client.post(f"/questions/search", json=search_data)
        # Extract the data from the response in JSON format
        data = json.loads(res.data)
        
        # Check status code
        self.assertEqual(res.status_code, 200)
        # Check for expected fields in the response
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["questions"]), 1)
        self.assertEqual(data["total_questions"], 1)
        # Check if content is correct
        for question in data["questions"]:
            self.assertIn("larg", question["question"].lower())
    

    def test_search_questions_with_no_results(self):
        # Payload to send
        search_data = {"searchTerm": "123-doesntexist"}
        # Get response object
        res = self.client.post(f"/questions/search", json=search_data)
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Check status code
        self.assertEqual(res.status_code, 200)
        # Check for expected fields in the response
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["questions"]), 0)
        self.assertEqual(data["total_questions"], 0)
    

    def test_405_if_search_attempted_with_delete(self):
        # Get response object
        res = self.client.delete(f"/questions/search")
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Assert that the method is not allowed
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")
    

    def test_405_if_search_attempted_with_get(self):
        # Get response object
        res = self.client.get(f"/questions/search")
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Assert that the method is not allowed
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    
    def test_405_if_search_attempted_with_patch(self):
        # Get response object
        res = self.client.patch(f"/questions/search")
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Assert that the method is not allowed
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")
    

    def test_405_if_search_attempted_with_put(self):
        # Get response object
        res = self.client.put(f"/questions/search")
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Assert that the method is not allowed
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")
    

    # Test get questions by category
    def test_get_questions_by_category(self):
        # Get response object
        res = self.client.get(f"/categories/1/questions")
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Check status code
        self.assertEqual(res.status_code, 200)
        # Check for expected fields in the response
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        # Check that the category of the questions is the expected one
        for question in data["questions"]:
            self.assertEqual(question["category"], "1")


    def test_404_if_get_questions_for_invalid_category(self):
        # Get response object
        res = self.client.get(f"/categories/1000/questions")
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Check status code
        self.assertEqual(res.status_code, 404)
        # Check for expected fields in the response
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
    

    def test_405_if_get_questions_by_category_with_delete(self):
        # Get response object
        res = self.client.delete(f"/categories/1/questions")
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Assert that the method is not allowed
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    
    def test_405_if_get_questions_by_category_with_patch(self):
        # Get response object
        res = self.client.patch(f"/categories/1/questions")
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Assert that the method is not allowed
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")
    

    def test_405_if_get_questions_by_category_with_post(self):
        # Get response object
        res = self.client.post(f"/categories/1/questions")
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Assert that the method is not allowed
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")
    

    def test_405_if_get_questions_by_category_with_put(self):
        # Get response object
        res = self.client.put(f"/categories/1/questions")
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Assert that the method is not allowed
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")


    # Test quiz endpoint
    def test_quiz_endpoint(self):
        # Define payload
        payload = {
            "previous_questions": [1, 5, 10],
            "quiz_category": {
                "id": "2",
                "type": "Art"
            }
        }
        # Get response object
        res = self.client.post("/quizzes", json=payload)
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Check status code
        self.assertEqual(res.status_code, 200)
        # Check for expected fields in the response
        self.assertEqual(data["success"], True)
        self.assertNotIn(data["question"]["id"], payload["previous_questions"])
        self.assertTrue(data["question"]["question"])
        self.assertTrue(data["question"]["answer"])
        self.assertEqual(data["question"]["category"], payload["quiz_category"]["id"])
        self.assertTrue(data["question"]["difficulty"])
    

    # Test quiz endpoint for 'All' category
    def test_quiz_endpoint_for_all_category(self):
        # Define payload
        payload = {
            "previous_questions": [1, 5, 10],
            "quiz_category": {
                "id": 0,
                "type": "All"
            }
        }
        # Get response object
        res = self.client.post("/quizzes", json=payload)
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Check status code
        self.assertEqual(res.status_code, 200)
        # Check for expected fields in the response
        self.assertEqual(data["success"], True)
        self.assertNotIn(data["question"]["id"], payload["previous_questions"])
        self.assertTrue(data["question"]["question"])
        self.assertTrue(data["question"]["answer"])
        self.assertTrue(data["question"]["difficulty"])
    

    #Tests that a 400 Bad Request error is returned 
    # when the request body is not valid JSON.
    def test_400_if_quiz_body_is_malformed_json(self):
        # Send a request with a malformed JSON body
        res = self.client.post(
            '/quizzes',
            data='this is not valid json',
            content_type='application/json'
        )
        data = json.loads(res.data)

        # Assert that the request is a bad request
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    

    # Tests that a 422 Unprocessable error is returned when the JSON
    # body is a valid JSON type (e.g., list) but not the expected object.
    def test_422_if_quiz_body_has_wrong_type(self):
        # Payload is a list instead of the expected dictionary
        payload = []
        
        # Make the request
        res = self.client.post('/quizzes', json=payload)
        data = json.loads(res.data)

        # Assert that the request is unprocessable
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


    def test_end_of_quiz(self):
        # Add all the available questions numbers to the payload
        with self.app.app_context():
            questions_in_category = Question.query.filter(Question.category == '2').all()
            previous_ids = [ question.id for question in questions_in_category ]
        # Payload
        payload = {
            'previous_questions': previous_ids,
            'quiz_category': { 'id': '2', 'type': 'Art' }
        }
        # Get response object
        res = self.client.post("/quizzes", json=payload)
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Check status code
        self.assertEqual(res.status_code, 200)
        # Check for expected fields in the response
        self.assertEqual(data["success"], True)
        self.assertIsNone(data["question"])
    

    def test_405_if_quiz_started_with_delete(self):
        # Get response object
        res = self.client.delete("/quizzes")
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Check status code
        self.assertEqual(res.status_code, 405)
        # Check for expected fields in the response
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")
    

    def test_405_if_quiz_started_with_get(self):
        # Get response object
        res = self.client.get("/quizzes")
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Check status code
        self.assertEqual(res.status_code, 405)
        # Check for expected fields in the response
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")
    

    def test_405_if_quiz_started_with_patch(self):
        # Get response object
        res = self.client.patch("/quizzes")
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Check status code
        self.assertEqual(res.status_code, 405)
        # Check for expected fields in the response
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")
    

    def test_405_if_quiz_started_with_put(self):
        # Get response object
        res = self.client.put("/quizzes")
        # Extract the data from the response in JSON format
        data = json.loads(res.data)

        # Check status code
        self.assertEqual(res.status_code, 405)
        # Check for expected fields in the response
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")
    

    def test_422_if_quiz_fails_with_missing_data(self):
        # Payload that is missing the 'previous_questions' key
        payload = {
            'quiz_category': { 'id': '1', 'type': 'Science' }
        }

        # Make the request
        res = self.client.post('/quizzes', json=payload)
        data = json.loads(res.data)

        # Assert that the request is unprocessable
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
