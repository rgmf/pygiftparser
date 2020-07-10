import unittest

from pygiftparser import parser
from pygiftparser.gift import MultipleChoiceRadio


class TestMultipleChoiceRadioQuestion(unittest.TestCase):
    def setUp(self):
        self.result = parser.parse(
            """
            Who's buried in Grant's tomb? {
                =Grant
                ~no one
                ~Napoleon
                ~Churchill
                ~Mother Teresa
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
        self.assertTrue(isinstance(self.answer, MultipleChoiceRadio))


    def test_number_of_questions(self):
        self.assertEqual(len(self.result.questions), 1)


    def test_name_and_text_of_questions(self):
        self.assertEqual(self.question.name, "Who's buried in Grant's tomb?")
        self.assertEqual(self.question.text, "Who's buried in Grant's tomb?")
        self.assertEqual(self.question.text_continue, None)


    def test_answer(self):
        self.assertEqual(len(self.answer.options), 5)


    def test_options(self):
        self.assertEqual(self.options[0].prefix, '=')
        self.assertEqual(self.options[0].text, 'Grant')
        self.assertEqual(self.options[0].raw_text, '=Grant')
        self.assertEqual(self.options[0].percentage, 1.0)

        self.assertEqual(self.options[1].prefix, '~')
        self.assertEqual(self.options[1].text, 'no one')
        self.assertEqual(self.options[1].raw_text, '~no one')
        self.assertEqual(self.options[1].percentage, 0.0)

        self.assertEqual(self.options[2].prefix, '~')
        self.assertEqual(self.options[2].text, 'Napoleon')
        self.assertEqual(self.options[2].raw_text, '~Napoleon')
        self.assertEqual(self.options[2].percentage, 0.0)

        self.assertEqual(self.options[3].prefix, '~')
        self.assertEqual(self.options[3].text, 'Churchill')
        self.assertEqual(self.options[3].raw_text, '~Churchill')
        self.assertEqual(self.options[3].percentage, 0.0)

        self.assertEqual(self.options[4].prefix, '~')
        self.assertEqual(self.options[4].text, 'Mother Teresa')
        self.assertEqual(self.options[4].raw_text, '~Mother Teresa')
        self.assertEqual(self.options[4].percentage, 0.0)


class TestMultipleChoiceRadioQuestion1(TestMultipleChoiceRadioQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            Who's buried in Grant's tomb?{=Grant~no one~Napoleon~Churchill~Mother Teresa}
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


class TestMultipleChoiceRadioQuestion2(TestMultipleChoiceRadioQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            Who's
            buried
            \tin\t
            Grant's tomb?{=Grant~no one~Napoleon~Churchill~Mother Teresa}
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


class TestMultipleChoiceRadioQuestion3(TestMultipleChoiceRadioQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            Who's buried in Grant's tomb?
            {
                
                =Grant
                
                ~no one
                
                ~Napoleon
                
                
                ~Churchill
                
                ~Mother Teresa
                
            }
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


class TestMultipleChoiceRadioQuestionWithName(TestMultipleChoiceRadioQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            ::The best: name of a question::Who's buried in Grant's tomb?
            {
                =Grant                ~no one
                ~Napoleon~Churchill
                ~Mother Teresa
            }
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def test_name_and_text_of_questions(self):
        self.assertEqual(self.question.name, "The best: name of a question")
        self.assertEqual(self.question.text, "Who's buried in Grant's tomb?")
        self.assertEqual(self.question.text_continue, None)


class TestMultipleChoiceRadioWithContinue(TestMultipleChoiceRadioQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            ::With name::Who's buried in Grant's tomb? {
                =Grant
                ~no one
                ~Napoleon
                ~Churchill
                ~Mother Teresa
            }
            with continue text.
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def test_name_and_text_of_questions(self):
        self.assertEqual(self.question.name, "With name")
        self.assertEqual(self.question.text, "Who's buried in Grant's tomb?")
        self.assertEqual(self.question.text_continue, 'with continue text.')


class TestMultipleChoiceRadioQuestionError(unittest.TestCase):
    def test_error_not_closed_bracket(self):
        with self.assertRaises(Exception):
            self.result = parser.parse(
                """
                Who's buried in Grant's tomb?
                    =Grant
                    ~no one
                    ~Napoleon
                    ~Churchill
                    ~Mother Teresa
                }
                """
            )


    def test_error_not_opened_bracket(self):
        with self.assertRaises(Exception):
            self.result = parser.parse(
                """
                Who's buried in Grant's tomb? {
                    =Grant
                    ~no one
                    ~Napoleon
                    ~Churchill
                    ~Mother Teresa
                """
            )