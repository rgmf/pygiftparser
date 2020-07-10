import unittest

from pygiftparser import parser
from pygiftparser.gift import Range, Numerical


class TestNumericalRangeQuestion(unittest.TestCase):
    def setUp(self):
        self.result = parser.parse(
            """
            What is the value of pi (to 3 decimal places)? {#3.141..3.142}
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def tearDown(self):
        self.result.questions = []
        self.result = None


    def test_type_of_answer(self):
        self.assertTrue(isinstance(self.answer, Range))


    def test_number_of_questions(self):
        self.assertEqual(len(self.result.questions), 1)


    def test_name_and_text_of_questions(self):
        self.assertEqual(self.question.name, "What is the value of pi (to 3 decimal places)?")
        self.assertEqual(self.question.text, "What is the value of pi (to 3 decimal places)?")
        self.assertEqual(self.question.text_continue, None)


    def test_answer(self):
        self.assertEqual(len(self.answer.options), 1)


    def test_options(self):
        self.assertEqual(self.options[0].prefix, '#')
        self.assertEqual(self.options[0].text, '3.141..3.142')
        self.assertEqual(self.options[0].raw_text, '#3.141..3.142')
        self.assertEqual(self.options[0].percentage, 1.0)
        self.assertEqual(self.options[0].feedback, None)

        self.assertIsNotNone(self.answer.number_from)
        self.assertIsNotNone(self.answer.number_to)

        numerical_from = self.answer.number_from
        self.assertIsInstance(numerical_from, Numerical)

        numerical_to = self.answer.number_to
        self.assertIsInstance(numerical_to, Numerical)

        self.assertEqual(len(numerical_from.options), 1)
        self.assertEqual(len(numerical_to.options), 1)

        self.assertEqual(numerical_from.options[0].prefix, '#')
        self.assertEqual(numerical_from.options[0].text, '3.141')
        self.assertEqual(numerical_from.options[0].raw_text, '#3.141')
        self.assertEqual(numerical_from.options[0].percentage, 1.0)
        self.assertEqual(numerical_from.options[0].feedback, None)
        self.assertEqual(numerical_from.get_number(), 3.141)
        self.assertEqual(numerical_from.get_error_margin(), 0.0)

        self.assertEqual(numerical_to.options[0].prefix, '#')
        self.assertEqual(numerical_to.options[0].text, '3.142')
        self.assertEqual(numerical_to.options[0].raw_text, '#3.142')
        self.assertEqual(numerical_to.options[0].percentage, 1.0)
        self.assertEqual(numerical_to.options[0].feedback, None)
        self.assertEqual(numerical_to.get_number(), 3.142)
        self.assertEqual(numerical_to.get_error_margin(), 0.0)


class TestNumericalRangeQuestionWithFeedback(TestNumericalRangeQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            What is the value of pi (to 3 decimal places)? {#3.141..3.142#This is a feedback}
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def test_answer(self):
        self.assertEqual(len(self.answer.options), 1)


    def test_options(self):
        self.assertEqual(self.options[0].prefix, '#')
        self.assertEqual(self.options[0].text, '3.141..3.142')
        self.assertEqual(self.options[0].raw_text, '#3.141..3.142')
        self.assertEqual(self.options[0].percentage, 1.0)
        self.assertEqual(self.options[0].feedback, 'This is a feedback')

        self.assertIsNotNone(self.answer.number_from)
        self.assertIsNotNone(self.answer.number_to)

        numerical_from = self.answer.number_from
        self.assertIsInstance(numerical_from, Numerical)

        numerical_to = self.answer.number_to
        self.assertIsInstance(numerical_to, Numerical)

        self.assertEqual(len(numerical_from.options), 1)
        self.assertEqual(len(numerical_to.options), 1)

        self.assertEqual(numerical_from.options[0].prefix, '#')
        self.assertEqual(numerical_from.options[0].text, '3.141')
        self.assertEqual(numerical_from.options[0].raw_text, '#3.141')
        self.assertEqual(numerical_from.options[0].percentage, 1.0)
        self.assertEqual(numerical_from.options[0].feedback, None)

        self.assertEqual(numerical_to.options[0].prefix, '#')
        self.assertEqual(numerical_to.options[0].text, '3.142')
        self.assertEqual(numerical_to.options[0].raw_text, '#3.142')
        self.assertEqual(numerical_to.options[0].percentage, 1.0)
        self.assertEqual(numerical_to.options[0].feedback, None)


class TestNumericalRangeQuestionWithFeedbackAndName(TestNumericalRangeQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            ::Question's name::What is the value of pi (to 3 decimal places)? {#3.141..3.142#This is a feedback}
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def test_answer(self):
        self.assertEqual(len(self.answer.options), 1)


    def test_name_and_text_of_questions(self):
        self.assertEqual(self.question.name, "Question's name")
        self.assertEqual(self.question.text, "What is the value of pi (to 3 decimal places)?")
        self.assertEqual(self.question.text_continue, None)


    def test_options(self):
        self.assertEqual(self.options[0].prefix, '#')
        self.assertEqual(self.options[0].text, '3.141..3.142')
        self.assertEqual(self.options[0].raw_text, '#3.141..3.142')
        self.assertEqual(self.options[0].percentage, 1.0)
        self.assertEqual(self.options[0].feedback, 'This is a feedback')

        self.assertIsNotNone(self.answer.number_from)
        self.assertIsNotNone(self.answer.number_to)

        numerical_from = self.answer.number_from
        self.assertIsInstance(numerical_from, Numerical)

        numerical_to = self.answer.number_to
        self.assertIsInstance(numerical_to, Numerical)

        self.assertEqual(len(numerical_from.options), 1)
        self.assertEqual(len(numerical_to.options), 1)

        self.assertEqual(numerical_from.options[0].prefix, '#')
        self.assertEqual(numerical_from.options[0].text, '3.141')
        self.assertEqual(numerical_from.options[0].raw_text, '#3.141')
        self.assertEqual(numerical_from.options[0].percentage, 1.0)
        self.assertEqual(numerical_from.options[0].feedback, None)

        self.assertEqual(numerical_to.options[0].prefix, '#')
        self.assertEqual(numerical_to.options[0].text, '3.142')
        self.assertEqual(numerical_to.options[0].raw_text, '#3.142')
        self.assertEqual(numerical_to.options[0].percentage, 1.0)
        self.assertEqual(numerical_to.options[0].feedback, None)


class TestNumericalRangeQuestionWithFeedbackAndNameAndTextContinuation(TestNumericalRangeQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            ::Question's name::What is the value of pi (to 3 decimal places)? {
                #3.141..3.142#This is a feedback
            }.
            This is the continuation.
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def test_answer(self):
        self.assertEqual(len(self.answer.options), 1)


    def test_name_and_text_of_questions(self):
        self.assertEqual(self.question.name, "Question's name")
        self.assertEqual(self.question.text, "What is the value of pi (to 3 decimal places)?")
        self.assertEqual(self.question.text_continue, '. This is the continuation.')


    def test_options(self):
        self.assertEqual(self.options[0].prefix, '#')
        self.assertEqual(self.options[0].text, '3.141..3.142')
        self.assertEqual(self.options[0].raw_text, '#3.141..3.142')
        self.assertEqual(self.options[0].percentage, 1.0)
        self.assertEqual(self.options[0].feedback, 'This is a feedback')

        self.assertIsNotNone(self.answer.number_from)
        self.assertIsNotNone(self.answer.number_to)

        numerical_from = self.answer.number_from
        self.assertIsInstance(numerical_from, Numerical)

        numerical_to = self.answer.number_to
        self.assertIsInstance(numerical_to, Numerical)

        self.assertEqual(len(numerical_from.options), 1)
        self.assertEqual(len(numerical_to.options), 1)

        self.assertEqual(numerical_from.options[0].prefix, '#')
        self.assertEqual(numerical_from.options[0].text, '3.141')
        self.assertEqual(numerical_from.options[0].raw_text, '#3.141')
        self.assertEqual(numerical_from.options[0].percentage, 1.0)
        self.assertEqual(numerical_from.options[0].feedback, None)

        self.assertEqual(numerical_to.options[0].prefix, '#')
        self.assertEqual(numerical_to.options[0].text, '3.142')
        self.assertEqual(numerical_to.options[0].raw_text, '#3.142')
        self.assertEqual(numerical_to.options[0].percentage, 1.0)
        self.assertEqual(numerical_to.options[0].feedback, None)


class TestNumericalRangeQuestionError(unittest.TestCase):
    def test_error_not_valid_number1(self):
        with self.assertRaises(Exception):
            self.result = parser.parse(
            "::Question's name::What is the value of pi (to 3 decimal places)? {#3.141..3.142 ~no =sí}"
        )


    def test_error_not_valid_number2(self):
        with self.assertRaises(Exception):
            self.result = parser.parse(
            "::Question's name::What is the value of pi (to 3 decimal places)? {#3.hello..3.142}"
        )


    def test_error_not_valid_number3(self):
        with self.assertRaises(Exception):
            self.result = parser.parse(
            "::Question's name::What is the value of pi (to 3 decimal places)? {#3.141..bye.142}"
        )


    def test_error_not_valid_number4(self):
        with self.assertRaises(Exception):
            self.result = parser.parse(
            "::Question's name::What is the value of pi (to 3 decimal places)? {#3.141.3.142}"
        )


    def test_error_not_valid_number5(self):
        with self.assertRaises(Exception):
            self.result = parser.parse(
            "::Question's name::What is the value of pi (to 3 decimal places)? {#3.141 .. 3.142}"
        )
