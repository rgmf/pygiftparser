import unittest

from pygiftparser import parser
from pygiftparser.gift import TrueFalse


class TestTrueFalseQuestion(unittest.TestCase):
    def setUp(self):
        self.result = parser.parse(
            """
            // True false questions.

            Grant was buried in a tomb in New York City.{T}
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def tearDown(self):
        self.result.questions = []
        self.result = None


    def test_type_of_answer(self):
        self.assertTrue(isinstance(self.answer, TrueFalse))


    def test_number_of_questions(self):
        self.assertEqual(len(self.result.questions), 1)


    def test_name_and_text_of_questions(self):
        self.assertEqual(self.question.name, "Grant was buried in a tomb in New York City.")
        self.assertEqual(self.question.text, "Grant was buried in a tomb in New York City.")
        self.assertEqual(self.question.text_continue, None)


    def test_answer(self):
        self.assertEqual(len(self.answer.options), 1)


class TestTrueQuestion(TestTrueFalseQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            // True false questions.

            Grant was buried in a tomb in New York City.{T}
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def test_options(self):
        self.assertEqual(self.options[0].prefix, None)
        self.assertEqual(self.options[0].text, 'True')
        self.assertEqual(self.options[0].raw_text, 'True')
        self.assertEqual(self.options[0].percentage, 1.0)
        self.assertEqual(self.options[0].feedback, None)


class TestTrueQuestionWithFeedback(TestTrueFalseQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            // True false questions.

            Grant was buried in a tomb in New York City.{T#feedback 1}
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def test_options(self):
        self.assertEqual(self.options[0].prefix, None)
        self.assertEqual(self.options[0].text, 'True')
        self.assertEqual(self.options[0].raw_text, 'True')
        self.assertEqual(self.options[0].percentage, 1.0)
        self.assertEqual(self.options[0].feedback, 'feedback 1')


class TestFalseQuestion(TestTrueFalseQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            // True false questions.

            Grant was buried in a tomb in New York City.{F}
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def test_options(self):
        self.assertEqual(self.options[0].prefix, None)
        self.assertEqual(self.options[0].text, 'False')
        self.assertEqual(self.options[0].raw_text, 'False')
        self.assertEqual(self.options[0].percentage, 1.0)
        self.assertEqual(self.options[0].feedback, None)


class TestFalseQuestionWithFeedback(TestTrueFalseQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            // True false questions.

            Grant was buried in a tomb in New York City.{F# feedback here}
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def test_options(self):
        self.assertEqual(self.options[0].prefix, None)
        self.assertEqual(self.options[0].text, 'False')
        self.assertEqual(self.options[0].raw_text, 'False')
        self.assertEqual(self.options[0].percentage, 1.0)
        self.assertEqual(self.options[0].feedback, 'feedback here')


class TestTrueQuestion1(TestTrueQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            // True false questions.

            Grant was buried in a tomb in New York City.{t}
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


class TestTrueQuestion2(TestTrueQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            // True false questions.

            Grant was buried in a tomb in New York City.{TRUE}
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


class TestTrueQuestion3(TestTrueQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            // True false questions.

            Grant was buried in a tomb in New York City.{true}
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


class TestFalseQuestion1(TestFalseQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            // True false questions.

            Grant was buried in a tomb in New York City.{f}
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


class TestFalseQuestion2(TestFalseQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            // True false questions.

            Grant was buried in a tomb in New York City.{FALSE}
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


class TestFalseQuestion3(TestFalseQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            // True false questions.

            Grant was buried in a tomb in New York City.{false}
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


class TestTrueQuestionWithName(TestTrueQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            // True false questions.

            ::This is the name::Grant was buried in a tomb in New York City.{t}
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def test_name_and_text_of_questions(self):
        self.assertEqual(self.question.name, "This is the name")
        self.assertEqual(self.question.text, "Grant was buried in a tomb in New York City.")
        self.assertEqual(self.question.text_continue, None)


class TestFalseQuestionWithName(TestFalseQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            // True false questions.

            ::This is the name::Grant was buried in a tomb in New York City.{f}
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def test_name_and_text_of_questions(self):
        self.assertEqual(self.question.name, "This is the name")
        self.assertEqual(self.question.text, "Grant was buried in a tomb in New York City.")
        self.assertEqual(self.question.text_continue, None)


class TestTrueFalseQuestionError(unittest.TestCase):
    def test_error_not_closed_bracket(self):
        with self.assertRaises(Exception):
            self.result = parser.parse(
                """
                ::This is the name::Grant was buried in a tomb in New York City.{f
                """
            )


    def test_error_not_opened_bracket(self):
        with self.assertRaises(Exception):
            self.result = parser.parse(
                """
                ::This is the name::Grant was buried in a tomb in New York City.f}
                """
            )
