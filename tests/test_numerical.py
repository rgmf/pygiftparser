import unittest

from pygiftparser import parser
from pygiftparser.gift import Numerical


class TestNumericalQuestion(unittest.TestCase):
    def setUp(self):
        self.result = parser.parse(
            """
            When was Ulysses S. Grant born?{#1822:5}
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def tearDown(self):
        self.result.questions = []
        self.result = None


    def test_type_of_answer(self):
        self.assertTrue(isinstance(self.answer, Numerical))


    def test_number_of_questions(self):
        self.assertEqual(len(self.result.questions), 1)


    def test_name_and_text_of_questions(self):
        self.assertEqual(self.question.name, "When was Ulysses S. Grant born?")
        self.assertEqual(self.question.text, "When was Ulysses S. Grant born?")
        self.assertEqual(self.question.text_continue, None)


    def test_answer(self):
        self.assertEqual(len(self.answer.options), 1)


    def test_options(self):
        self.assertEqual(self.options[0].prefix, '#')
        self.assertEqual(self.options[0].text, '1822:5')
        self.assertEqual(self.options[0].raw_text, '#1822:5')
        self.assertEqual(self.options[0].percentage, 1.0)
        self.assertEqual(self.options[0].feedback, None)
        self.assertEqual(self.answer.get_number(), 1822.0)
        self.assertEqual(self.answer.get_error_margin(), 5.0)


class TestNumericalQuestion2(TestNumericalQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            When was Ulysses S. Grant born? {
                #1822.54:10.04
            }
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def test_options(self):
        self.assertEqual(self.options[0].prefix, '#')
        self.assertEqual(self.options[0].text, '1822.54:10.04')
        self.assertEqual(self.options[0].raw_text, '#1822.54:10.04')
        self.assertEqual(self.options[0].percentage, 1.0)
        self.assertEqual(self.options[0].feedback, None)
        self.assertEqual(self.answer.get_number(), 1822.54)
        self.assertEqual(self.answer.get_error_margin(), 10.04)


class TestNumericalQuestion3(TestNumericalQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            ::With name::What is the value of pi (to 3 decimal places)?
            {
                #3.14159:0.0005
            }.
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def test_name_and_text_of_questions(self):
        self.assertEqual(self.question.name, "With name")
        self.assertEqual(self.question.text, "What is the value of pi (to 3 decimal places)?")
        self.assertEqual(self.question.text_continue, '.')


    def test_options(self):
        self.assertEqual(self.options[0].prefix, '#')
        self.assertEqual(self.options[0].text, '3.14159:0.0005')
        self.assertEqual(self.options[0].raw_text, '#3.14159:0.0005')
        self.assertEqual(self.options[0].percentage, 1.0)
        self.assertEqual(self.options[0].feedback, None)
        self.assertEqual(self.answer.get_number(), 3.14159)
        self.assertEqual(self.answer.get_error_margin(), 0.0005)


class TestNumericalQuestionWithFeedback(TestNumericalQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            ::With name::What is the value of pi (to 3 decimal places)?
            {
                #3.14159:0.0005 # This is a feedback
            }.
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def test_name_and_text_of_questions(self):
        self.assertEqual(self.question.name, "With name")
        self.assertEqual(self.question.text, "What is the value of pi (to 3 decimal places)?")
        self.assertEqual(self.question.text_continue, '.')


    def test_options(self):
        self.assertEqual(self.options[0].prefix, '#')
        self.assertEqual(self.options[0].text, '3.14159:0.0005')
        self.assertEqual(self.options[0].raw_text, '#3.14159:0.0005')
        self.assertEqual(self.options[0].percentage, 1.0)
        self.assertEqual(self.options[0].feedback, 'This is a feedback')
        self.assertEqual(self.answer.get_number(), 3.14159)
        self.assertEqual(self.answer.get_error_margin(), 0.0005)


class TestNumericalQuestionError(unittest.TestCase):
    def test_error_not_valid_number1(self):
        with self.assertRaises(Exception):
            self.result = parser.parse(
            'When was Ulysses S. Grant born?{#hello}'
        )


    def test_error_not_valid_number2(self):
        with self.assertRaises(Exception):
            self.result = parser.parse(
            'When was Ulysses S. Grant born?{#1922:h}'
        )


    def test_error_not_valid_number3(self):
        with self.assertRaises(Exception):
            self.result = parser.parse(
            'When was Ulysses S. Grant born?{#hel:lo}'
        )


    def test_error_open_bracket(self):
        with self.assertRaises(Exception):
            self.result = parser.parse(
            'When was Ulysses S. Grant born? #100:2}'
        )


    def test_error_close_bracket(self):
        with self.assertRaises(Exception):
            self.result = parser.parse(
            'When was Ulysses S. Grant born? {#100:2'
        )