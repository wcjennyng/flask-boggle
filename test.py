from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Tests if information is in session and HTML is displayed"""
        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('playcount'))
            self.assertIn(b'High Score:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Timer:', response.data)

    def test_valid_word(self):
        """Test if word is valid"""
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["V", "A", "L", "I", "D"], 
                                 ["V", "A", "L", "I", "D"], 
                                 ["V", "A", "L", "I", "D"], 
                                 ["V", "A", "L", "I", "D"],
                                 ["V", "A", "L", "I", "D"]]
        response = self.client.get('/check-word?word=valid')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if word is in dictionary"""
        self.client.get('/')
        response = self.client.get('/check-word?word=nope')
        self.assertEqual(response.json['result'], 'not-on-board')


