import unittest

from pygiftparser import parser
from pygiftparser.gift import MultipleNumerical, Numerical, Range


class TestNumericalMultipleQuestion(unittest.TestCase):
    def setUp(self):
        self.result = parser.parse(
            """
            When was Ulysses S. Grant born? {#
                =1822:0
                =%50%1822:2
            }
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def tearDown(self):
        self.result.questions = []
        self.result = None


    def test_type_of_answer(self):
        self.assertTrue(isinstance(self.answer, MultipleNumerical))


    def test_number_of_questions(self):
        self.assertEqual(len(self.result.questions), 1)


    def test_name_and_text_of_questions(self):
        self.assertEqual(self.question.name, "When was Ulysses S. Grant born?")
        self.assertEqual(self.question.text, "When was Ulysses S. Grant born?")
        self.assertEqual(self.question.text_continue, None)


    def test_answer(self):
        self.assertEqual(len(self.answer.options), 2)


    def test_options(self):
        self.assertEqual(self.options[0].prefix, '#')
        self.assertEqual(self.options[0].text, '1822:0')
        self.assertEqual(self.options[0].raw_text, '#1822:0')
        self.assertEqual(self.options[0].percentage, 1.0)
        self.assertEqual(self.options[0].feedback, None)

        self.assertEqual(self.options[1].prefix, '#')
        self.assertEqual(self.options[1].text, '1822:2')
        self.assertEqual(self.options[1].raw_text, '#%50%1822:2')
        self.assertEqual(self.options[1].percentage, 0.5)
        self.assertEqual(self.options[1].feedback, None)


    def test_numbers(self):
        numbers = self.answer.numbers
        self.assertEqual(len(numbers), 2)
        self.assertIsInstance(numbers[0], Numerical)
        self.assertIsInstance(numbers[1], Numerical)

        self.assertEqual(numbers[0].options[0].prefix, '#')
        self.assertEqual(numbers[0].options[0].text, '1822:0')
        self.assertEqual(numbers[0].options[0].raw_text, '#1822:0')
        self.assertEqual(numbers[0].options[0].percentage, 1.0)
        self.assertEqual(numbers[0].options[0].feedback, None)
        self.assertEqual(numbers[0].get_number(), 1822.0)
        self.assertEqual(numbers[0].get_error_margin(), 0.0)

        self.assertEqual(numbers[1].options[0].prefix, '#')
        self.assertEqual(numbers[1].options[0].text, '1822:2')
        self.assertEqual(numbers[1].options[0].raw_text, '#%50%1822:2')
        self.assertEqual(numbers[1].options[0].percentage, 0.5)
        self.assertEqual(numbers[1].options[0].feedback, None)
        self.assertEqual(numbers[1].get_number(), 1822.0)
        self.assertEqual(numbers[1].get_error_margin(), 2.0)


class TestNumericalMultipleQuestionWithName(TestNumericalMultipleQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            ::This is the name::When was Ulysses S. Grant born? {#
                =1822:0
                =%50%1822:2
            }
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def test_name_and_text_of_questions(self):
        self.assertEqual(self.question.name, "This is the name")
        self.assertEqual(self.question.text, "When was Ulysses S. Grant born?")
        self.assertEqual(self.question.text_continue, None)


class TestNumericalMultipleQuestionWithFeedback(TestNumericalMultipleQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            When was Ulysses S. Grant born? {#
                =1822:0 # feedback 1
                =%50%1822:2 # feedback 2
            }
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def test_options(self):
        self.assertEqual(self.options[0].prefix, '#')
        self.assertEqual(self.options[0].text, '1822:0')
        self.assertEqual(self.options[0].raw_text, '#1822:0')
        self.assertEqual(self.options[0].percentage, 1.0)
        self.assertEqual(self.options[0].feedback, 'feedback 1')

        self.assertEqual(self.options[1].prefix, '#')
        self.assertEqual(self.options[1].text, '1822:2')
        self.assertEqual(self.options[1].raw_text, '#%50%1822:2')
        self.assertEqual(self.options[1].percentage, 0.5)
        self.assertEqual(self.options[1].feedback, 'feedback 2')


    def test_numbers(self):
        numbers = self.answer.numbers
        self.assertEqual(len(numbers), 2)
        self.assertIsInstance(numbers[0], Numerical)
        self.assertIsInstance(numbers[1], Numerical)

        self.assertEqual(numbers[0].options[0].prefix, '#')
        self.assertEqual(numbers[0].options[0].text, '1822:0')
        self.assertEqual(numbers[0].options[0].raw_text, '#1822:0')
        self.assertEqual(numbers[0].options[0].percentage, 1.0)
        self.assertEqual(numbers[0].options[0].feedback, 'feedback 1')
        self.assertEqual(numbers[0].get_number(), 1822.0)
        self.assertEqual(numbers[0].get_error_margin(), 0.0)

        self.assertEqual(numbers[1].options[0].prefix, '#')
        self.assertEqual(numbers[1].options[0].text, '1822:2')
        self.assertEqual(numbers[1].options[0].raw_text, '#%50%1822:2')
        self.assertEqual(numbers[1].options[0].percentage, 0.5)
        self.assertEqual(numbers[1].options[0].feedback, 'feedback 2')
        self.assertEqual(numbers[1].get_number(), 1822.0)
        self.assertEqual(numbers[1].get_error_margin(), 2.0)


class TestRangeMultipleQuestion(unittest.TestCase):
    def setUp(self):
        self.result = parser.parse(
            """
            When was Ulysses S. Grant born? {#
                =1821..1823 
                =%50%1824..1825
            }
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def tearDown(self):
        self.result.questions = []
        self.result = None


    def test_type_of_answer(self):
        self.assertTrue(isinstance(self.answer, MultipleNumerical))


    def test_number_of_questions(self):
        self.assertEqual(len(self.result.questions), 1)


    def test_name_and_text_of_questions(self):
        self.assertEqual(self.question.name, "When was Ulysses S. Grant born?")
        self.assertEqual(self.question.text, "When was Ulysses S. Grant born?")
        self.assertEqual(self.question.text_continue, None)


    def test_answer(self):
        self.assertEqual(len(self.answer.options), 2)


    def test_options(self):
        self.assertEqual(self.options[0].prefix, '#')
        self.assertEqual(self.options[0].text, '1821..1823')
        self.assertEqual(self.options[0].raw_text, '#1821..1823')
        self.assertEqual(self.options[0].percentage, 1.0)
        self.assertEqual(self.options[0].feedback, None)

        self.assertEqual(self.options[1].prefix, '#')
        self.assertEqual(self.options[1].text, '1824..1825')
        self.assertEqual(self.options[1].raw_text, '#%50%1824..1825')
        self.assertEqual(self.options[1].percentage, 0.5)
        self.assertEqual(self.options[1].feedback, None)


    def test_numbers(self):
        numbers = self.answer.numbers
        self.assertEqual(len(numbers), 2)
        self.assertIsInstance(numbers[0], Range)
        self.assertIsInstance(numbers[1], Range)

        self.assertEqual(numbers[0].options[0].prefix, '#')
        self.assertEqual(numbers[0].options[0].text, '1821..1823')
        self.assertEqual(numbers[0].options[0].raw_text, '#1821..1823')
        self.assertEqual(numbers[0].options[0].percentage, 1.0)
        self.assertEqual(numbers[0].options[0].feedback, None)

        self.assertEqual(numbers[1].options[0].prefix, '#')
        self.assertEqual(numbers[1].options[0].text, '1824..1825')
        self.assertEqual(numbers[1].options[0].raw_text, '#%50%1824..1825')
        self.assertEqual(numbers[1].options[0].percentage, 0.5)
        self.assertEqual(numbers[1].options[0].feedback, None)


    def test_ranges(self):
        numbers = self.answer.numbers
        self.assertEqual(len(numbers), 2)
        self.assertIsInstance(numbers[0], Range)
        self.assertIsInstance(numbers[1], Range)

        self.assertEqual(numbers[0].number_from.get_number(), 1821.0)
        self.assertEqual(numbers[0].number_from.get_error_margin(), 0.0)
        self.assertEqual(numbers[0].number_to.get_number(), 1823.0)
        self.assertEqual(numbers[0].number_to.get_error_margin(), 0.0)

        self.assertEqual(numbers[1].number_from.get_number(), 1824.0)
        self.assertEqual(numbers[1].number_from.get_error_margin(), 0.0)
        self.assertEqual(numbers[1].number_to.get_number(), 1825.0)
        self.assertEqual(numbers[1].number_to.get_error_margin(), 0.0)


class TestRangeMultipleQuestionWithName(TestRangeMultipleQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            ::This is the name::When was Ulysses S. Grant born? {#
                =1821..1823 
                =%50%1824..1825
            }
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def test_name_and_text_of_questions(self):
        self.assertEqual(self.question.name, "This is the name")
        self.assertEqual(self.question.text, "When was Ulysses S. Grant born?")
        self.assertEqual(self.question.text_continue, None)


class TestRangeMultipleQuestionWithFeedback(TestRangeMultipleQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            When was Ulysses S. Grant born? {#
                =1821..1823  # feedback 1
                =%50%1824..1825  # another feedback
            }
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def test_options(self):
        self.assertEqual(self.options[0].prefix, '#')
        self.assertEqual(self.options[0].text, '1821..1823')
        self.assertEqual(self.options[0].raw_text, '#1821..1823')
        self.assertEqual(self.options[0].percentage, 1.0)
        self.assertEqual(self.options[0].feedback, 'feedback 1')

        self.assertEqual(self.options[1].prefix, '#')
        self.assertEqual(self.options[1].text, '1824..1825')
        self.assertEqual(self.options[1].raw_text, '#%50%1824..1825')
        self.assertEqual(self.options[1].percentage, 0.5)
        self.assertEqual(self.options[1].feedback, 'another feedback')


    def test_numbers(self):
        numbers = self.answer.numbers
        self.assertEqual(len(numbers), 2)
        self.assertIsInstance(numbers[0], Range)
        self.assertIsInstance(numbers[1], Range)

        self.assertEqual(numbers[0].options[0].prefix, '#')
        self.assertEqual(numbers[0].options[0].text, '1821..1823')
        self.assertEqual(numbers[0].options[0].raw_text, '#1821..1823')
        self.assertEqual(numbers[0].options[0].percentage, 1.0)
        self.assertEqual(numbers[0].options[0].feedback, 'feedback 1')

        self.assertEqual(numbers[1].options[0].prefix, '#')
        self.assertEqual(numbers[1].options[0].text, '1824..1825')
        self.assertEqual(numbers[1].options[0].raw_text, '#%50%1824..1825')
        self.assertEqual(numbers[1].options[0].percentage, 0.5)
        self.assertEqual(numbers[1].options[0].feedback, 'another feedback')


class TestMultipleNumericalQuestionError(unittest.TestCase):
    def test_error_not_valid_number1(self):
        with self.assertRaises(Exception):
            self.result = parser.parse(
            """
            When was Ulysses S. Grant born? {#
                =182a..1823  # feedback 1
                =%50%1824..1825  # another feedback
            }
            """
        )


    def test_error_not_valid_number2(self):
        with self.assertRaises(Exception):
            self.result = parser.parse(
            """
            When was Ulysses S. Grant born? {#
                =1821..1823  # feedback 1
                =%50%182b..1825  # another feedback
            }
            """
        )


    def test_error_not_valid_number3(self):
        with self.assertRaises(Exception):
            self.result = parser.parse(
            """
            When was Ulysses S. Grant born? {#
                =1821..1823  # feedback 1
                =%50%1824..18a5  # another feedback
            }
            """
        )


    def test_error_open_bracket(self):
        with self.assertRaises(Exception):
            self.result = parser.parse(
            """
            When was Ulysses S. Grant born? #
                =1821..1823  # feedback 1
                =%50%1824..1825  # another feedback
            }
            """
        )


    def test_error_close_bracket(self):
        with self.assertRaises(Exception):
            self.result = parser.parse(
            """
            When was Ulysses S. Grant born? {#
                =1821..1823  # feedback 1
                =%50%1824..1825  # another feedback
            
            """
        )