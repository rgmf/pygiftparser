import unittest

from pygiftparser import parser
from pygiftparser.gift import MultipleChoiceCheckbox


class TestMultipleChoiceCheckboxQuestion(unittest.TestCase):
    def setUp(self):
        self.result = parser.parse(
            """
            // Multiple choice with multiple right answers.

            What two people are entombed in Grant's tomb? {
                ~%-100%No one            # Nooo, no es válido
                ~%50%Grant               # Muy bien
                ~%50%Grant's wife        # Perfecto.
                ~%-100%Grant's father    # No, esta no era.
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
        self.assertTrue(isinstance(self.answer, MultipleChoiceCheckbox))


    def test_number_of_questions(self):
        self.assertEqual(len(self.result.questions), 1)


    def test_name_and_text_of_questions(self):
        self.assertEqual(self.question.name, "What two people are entombed in Grant's tomb?")
        self.assertEqual(self.question.text, "What two people are entombed in Grant's tomb?")
        self.assertEqual(self.question.text_continue, None)


    def test_answer(self):
        self.assertEqual(len(self.answer.options), 4)


    def test_options(self):
        self.assertEqual(self.options[0].prefix, '~')
        self.assertEqual(self.options[0].text, 'No one')
        self.assertEqual(self.options[0].raw_text, '~%-100%No one')
        self.assertEqual(self.options[0].percentage, -1.0)
        self.assertEqual(self.options[0].feedback, 'Nooo, no es válido')

        self.assertEqual(self.options[1].prefix, '~')
        self.assertEqual(self.options[1].text, 'Grant')
        self.assertEqual(self.options[1].raw_text, '~%50%Grant')
        self.assertEqual(self.options[1].percentage, 0.5)
        self.assertEqual(self.options[1].feedback, 'Muy bien')

        self.assertEqual(self.options[2].prefix, '~')
        self.assertEqual(self.options[2].text, "Grant's wife")
        self.assertEqual(self.options[2].raw_text, "~%50%Grant's wife")
        self.assertEqual(self.options[2].percentage, 0.5)
        self.assertEqual(self.options[2].feedback, 'Perfecto.')

        self.assertEqual(self.options[3].prefix, '~')
        self.assertEqual(self.options[3].text, "Grant's father")
        self.assertEqual(self.options[3].raw_text, "~%-100%Grant's father")
        self.assertEqual(self.options[3].percentage, -1.0)
        self.assertEqual(self.options[3].feedback, 'No, esta no era.')


class TestMultipleChoiceCheckboxQuestion1(TestMultipleChoiceCheckboxQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            // Multiple choice with multiple right answers.
            What two people are entombed in Grant's tomb?{~%-100%No one# Nooo, no es válido~%50%Grant# Muy bien~%50%Grant's wife# Perfecto.~%-100%Grant's father# No, esta no era.}
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


class TestMultipleChoiceCheckboxQuestion2(TestMultipleChoiceCheckboxQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            // Multiple choice with multiple right answers.

            What two people are entombed in Grant's tomb? {
                ~%-100%No one            # Nooo, no es válido
            ~%50%Grant               # Muy bien
                ~%50%Grant's wife        # Perfecto.
                        ~%-100%Grant's father    # No, esta no era.
            }
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


class TestMultipleChoiceCheckboxQuestion3(TestMultipleChoiceCheckboxQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            // Multiple choice with multiple right answers.

            What two people are entombed in Grant's tomb? {
                ~%-100%No one
                # Nooo, no es válido
                ~%50%Grant         
                      # Muy bien
                ~%50%Grant's wife
                        # Perfecto.
                ~%-100%Grant's father    
                # No, esta no era.
            }
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


class TestMultipleChoiceCheckboxQuestionWithName(TestMultipleChoiceCheckboxQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            // Multiple choice with multiple right answers.

            ::With name\=4: yes::What two people are entombed in Grant's tomb? {
                ~%-100%No one            # Nooo, no es válido
                ~%50%Grant               # Muy bien
                ~%50%Grant's wife        # Perfecto.
                ~%-100%Grant's father    # No, esta no era.
            }
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def test_name_and_text_of_questions(self):
        self.assertEqual(self.question.name, "With name\=4: yes")
        self.assertEqual(self.question.text, "What two people are entombed in Grant's tomb?")
        self.assertEqual(self.question.text_continue, None)


class TestMultipleChoiceCheckboxQuestionWithContinue(TestMultipleChoiceCheckboxQuestion):
    def setUp(self):
        self.result = parser.parse(
            """
            // Multiple choice with multiple right answers.

            ::With name::What two people are entombed in Grant's tomb? {
                ~%-100%No one            # Nooo, no es válido
                ~%50%Grant               # Muy bien
                ~%50%Grant's wife        # Perfecto.
                ~%-100%Grant's father    # No, esta no era.
            }
            with continue text.
            """
        )
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def test_name_and_text_of_questions(self):
        self.assertEqual(self.question.name, "With name")
        self.assertEqual(self.question.text, "What two people are entombed in Grant's tomb?")
        self.assertEqual(self.question.text_continue, 'with continue text.')


class TestMultipleChoiceCheckboxQuestionError(unittest.TestCase):
    def test_error_not_closed_bracket(self):
        with self.assertRaises(Exception):
            self.result = parser.parse(
                """
            // Multiple choice with multiple right answers.

            What two people are entombed in Grant's tomb?
                ~%-100%No one            # Nooo, no es válido
                ~%50%Grant               # Muy bien
                ~%50%Grant's wife        # Perfecto.
                ~%-100%Grant's father    # No, esta no era.
            }
            """
            )


    def test_error_not_opened_bracket(self):
        with self.assertRaises(Exception):
            self.result = parser.parse(
                """
            // Multiple choice with multiple right answers.

            What two people are entombed in Grant's tomb? {
                ~%-100%No one            # Nooo, no es válido
                ~%50%Grant               # Muy bien
                ~%50%Grant's wife        # Perfecto.
                ~%-100%Grant's father    # No, esta no era.
            """
            )