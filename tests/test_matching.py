import unittest

from pygiftparser import parser
from pygiftparser.gift import Matching, Short


class TestMatchingQuestion(unittest.TestCase):
    def setUp(self):
        self.result = parser.parse(
            """
            // Matching.

            Match the following countries with their corresponding capitals. {
                =Canada -> Ottawa
                =Italy  -> Rome
                =Japan  -> Tokyo
                =India  -> New Delhi
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
        self.assertTrue(isinstance(self.answer, Matching))


    def test_number_of_questions(self):
        self.assertEqual(len(self.result.questions), 1)


    def test_name_and_text_of_questions(self):
        self.assertEqual(self.question.name, "Match the following countries with their corresponding capitals.")
        self.assertEqual(self.question.text, "Match the following countries with their corresponding capitals.")
        self.assertEqual(self.question.text_continue, None)


    def test_answer(self):
        self.assertEqual(len(self.answer.options), 4)


    def test_options(self):
        self.assertEqual(self.options[0].prefix, '=')
        self.assertEqual(self.options[0].text, 'Canada -> Ottawa')
        self.assertEqual(self.options[0].raw_text, '=Canada -> Ottawa')
        self.assertEqual(self.options[0].percentage, 1.0)
        self.assertEqual(self.answer.get_pair(self.options[0])['first'], 'Canada')
        self.assertEqual(self.answer.get_pair(self.options[0])['second'], 'Ottawa')

        self.assertEqual(self.options[1].prefix, '=')
        self.assertEqual(self.options[1].text, 'Italy  -> Rome')
        self.assertEqual(self.options[1].raw_text, '=Italy  -> Rome')
        self.assertEqual(self.options[1].percentage, 1.0)
        self.assertEqual(self.answer.get_pair(self.options[1])['first'], 'Italy')
        self.assertEqual(self.answer.get_pair(self.options[1])['second'], 'Rome')

        self.assertEqual(self.options[2].prefix, '=')
        self.assertEqual(self.options[2].text, 'Japan  -> Tokyo')
        self.assertEqual(self.options[2].raw_text, '=Japan  -> Tokyo')
        self.assertEqual(self.options[2].percentage, 1.0)
        self.assertEqual(self.answer.get_pair(self.options[2])['first'], 'Japan')
        self.assertEqual(self.answer.get_pair(self.options[2])['second'], 'Tokyo')

        self.assertEqual(self.options[3].prefix, '=')
        self.assertEqual(self.options[3].text, 'India  -> New Delhi')
        self.assertEqual(self.options[3].raw_text, '=India  -> New Delhi')
        self.assertEqual(self.options[3].percentage, 1.0)
        self.assertEqual(self.answer.get_pair(self.options[3])['first'], 'India')
        self.assertEqual(self.answer.get_pair(self.options[3])['second'], 'New Delhi')


class TestMatchingQuestion1(TestMatchingQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            // Matching.

            Match the following countries with their corresponding capitals.{=Canada->Ottawa=Italy->Rome=Japan->Tokyo=India->New Delhi}
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def test_options(self):
        self.assertEqual(self.options[0].prefix, '=')
        self.assertEqual(self.options[0].text, 'Canada->Ottawa')
        self.assertEqual(self.options[0].raw_text, '=Canada->Ottawa')
        self.assertEqual(self.options[0].percentage, 1.0)
        self.assertEqual(self.answer.get_pair(self.options[0])['first'], 'Canada')
        self.assertEqual(self.answer.get_pair(self.options[0])['second'], 'Ottawa')

        self.assertEqual(self.options[1].prefix, '=')
        self.assertEqual(self.options[1].text, 'Italy->Rome')
        self.assertEqual(self.options[1].raw_text, '=Italy->Rome')
        self.assertEqual(self.options[1].percentage, 1.0)
        self.assertEqual(self.answer.get_pair(self.options[1])['first'], 'Italy')
        self.assertEqual(self.answer.get_pair(self.options[1])['second'], 'Rome')

        self.assertEqual(self.options[2].prefix, '=')
        self.assertEqual(self.options[2].text, 'Japan->Tokyo')
        self.assertEqual(self.options[2].raw_text, '=Japan->Tokyo')
        self.assertEqual(self.options[2].percentage, 1.0)
        self.assertEqual(self.answer.get_pair(self.options[2])['first'], 'Japan')
        self.assertEqual(self.answer.get_pair(self.options[2])['second'], 'Tokyo')

        self.assertEqual(self.options[3].prefix, '=')
        self.assertEqual(self.options[3].text, 'India->New Delhi')
        self.assertEqual(self.options[3].raw_text, '=India->New Delhi')
        self.assertEqual(self.options[3].percentage, 1.0)
        self.assertEqual(self.answer.get_pair(self.options[3])['first'], 'India')
        self.assertEqual(self.answer.get_pair(self.options[3])['second'], 'New Delhi')


class TestMatchingQuestion2(TestMatchingQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            // Matching.

            Match the following countries with their corresponding capitals.{
                =four\\=4->four4
                =Italy->Rome
                =Japan->Tokyo
                =India->New Delhi
            }
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def test_options(self):
        self.assertEqual(self.options[0].prefix, '=')
        self.assertEqual(self.options[0].text, 'four\\=4->four4')
        self.assertEqual(self.options[0].raw_text, '=four\\=4->four4')
        self.assertEqual(self.options[0].percentage, 1.0)
        self.assertEqual(self.answer.get_pair(self.options[0])['first'], 'four\\=4')
        self.assertEqual(self.answer.get_pair(self.options[0])['second'], 'four4')

        self.assertEqual(self.options[1].prefix, '=')
        self.assertEqual(self.options[1].text, 'Italy->Rome')
        self.assertEqual(self.options[1].raw_text, '=Italy->Rome')
        self.assertEqual(self.options[1].percentage, 1.0)
        self.assertEqual(self.answer.get_pair(self.options[1])['first'], 'Italy')
        self.assertEqual(self.answer.get_pair(self.options[1])['second'], 'Rome')

        self.assertEqual(self.options[2].prefix, '=')
        self.assertEqual(self.options[2].text, 'Japan->Tokyo')
        self.assertEqual(self.options[2].raw_text, '=Japan->Tokyo')
        self.assertEqual(self.options[2].percentage, 1.0)
        self.assertEqual(self.answer.get_pair(self.options[2])['first'], 'Japan')
        self.assertEqual(self.answer.get_pair(self.options[2])['second'], 'Tokyo')

        self.assertEqual(self.options[3].prefix, '=')
        self.assertEqual(self.options[3].text, 'India->New Delhi')
        self.assertEqual(self.options[3].raw_text, '=India->New Delhi')
        self.assertEqual(self.options[3].percentage, 1.0)
        self.assertEqual(self.answer.get_pair(self.options[3])['first'], 'India')
        self.assertEqual(self.answer.get_pair(self.options[3])['second'], 'New Delhi')


class TestNotMatchingQuestion(unittest.TestCase):
    def setUp(self):
        self.result = parser.parse(
            """
            // Matching.

            Match the following countries with their corresponding capitals. {
                =Canada -> Ottawa
                =Italy  -> Rome
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
        self.assertTrue(isinstance(self.answer, Short))
        
        
    def test_answer(self):
        self.assertEqual(len(self.answer.options), 2)


class TestMatchingQuestion3(TestMatchingQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            // Matching.

            ::With name::Match the following countries with their corresponding capitals. {
                =Canada -> Ottawa
                =Italy  -> Rome
                =Japan  -> Tokyo
                =India  -> New Delhi
            }
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def test_name_and_text_of_questions(self):
        self.assertEqual(self.question.name, "With name")
        self.assertEqual(self.question.text, "Match the following countries with their corresponding capitals.")
        self.assertEqual(self.question.text_continue, None)


class TestMatchingQuestionWithContinue(TestMatchingQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            // Matching.

            ::With name::Match the following countries with their corresponding capitals. {
                =Canada -> Ottawa
                =Italy  -> Rome
                =Japan  -> Tokyo
                =India  -> New Delhi
            }
            with continue text.
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def test_name_and_text_of_questions(self):
        self.assertEqual(self.question.name, "With name")
        self.assertEqual(self.question.text, "Match the following countries with their corresponding capitals.")
        self.assertEqual(self.question.text_continue, 'with continue text.')


class TestMatchingQuestionError(unittest.TestCase):
    def test_error_not_closed_bracket(self):
        with self.assertRaises(Exception):
            self.result = parser.parse(
            """
            // Matching.

            Match the following countries with their corresponding capitals. {
                =Canada -> Ottawa
                =Italy  -> Rome
                =Japan  -> Tokyo
                =India  -> New Delhi
            """
        )


    def test_error_not_opened_bracket(self):
        with self.assertRaises(Exception):
            self.result = parser.parse(
            """
            // Matching.

            Match the following countries with their corresponding capitals.
                =Canada -> Ottawa
                =Italy  -> Rome
                =Japan  -> Tokyo
                =India  -> New Delhi
            }
            """
        )
