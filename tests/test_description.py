import unittest

from pygiftparser import parser
from pygiftparser.gift import Description


class TestDescriptionQuestion(unittest.TestCase):
    def setUp(self):
        self.result = parser.parse(
            """
            // Description.

            Write a short biography of Dag Hammarskjöld.
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def tearDown(self):
        self.result.questions = []
        self.result = None


    def test_type_of_answer(self):
        self.assertTrue(isinstance(self.answer, Description))


    def test_number_of_questions(self):
        self.assertEqual(len(self.result.questions), 1)


    def test_name_and_text_of_questions(self):
        self.assertEqual(self.question.name, "Write a short biography of Dag Hammarskjöld.")
        self.assertEqual(self.question.text, "Write a short biography of Dag Hammarskjöld.")
        self.assertEqual(self.question.text_continue, None)


    def test_answer(self):
        self.assertEqual(len(self.answer.options), 0)


class TestDescriptionQuestionWithName(TestDescriptionQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            // Description.

            ::This is the name of the question::
            Write a short biography of Dag Hammarskjöld.
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def test_name_and_text_of_questions(self):
        self.assertEqual(self.question.name, "This is the name of the question")
        self.assertEqual(self.question.text, "Write a short biography of Dag Hammarskjöld.")
        self.assertEqual(self.question.text_continue, None)
