import unittest

from pygiftparser import parser
from pygiftparser.gift import TrueFalse


class TestEscapingQuestionTitle(unittest.TestCase):
    def setUp(self):
        self.result = parser.parse(
            """
            ::Characters in Title\: \~ \= \# \{ \}:: Question text {T}            
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options

    def tearDown(self):
        self.result.questions = []
        self.result = None

    def test_escaping_in_question_text_is_unescaped(self):
        self.assertEqual(self.question.name, "Characters in Title: ~ = # { }")


class TestEscapingQuestionText(unittest.TestCase):
    def setUp(self):
        self.result = parser.parse(
            """
            ::Title:: Special characters in question\: \~ \= \# \{ \} {T}            
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options

    def tearDown(self):
        self.result.questions = []
        self.result = None

    def test_escaping_in_question_text_is_unescaped(self):
        self.assertEqual(self.question.text, "Special characters in question: ~ = # { }")