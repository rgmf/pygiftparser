import unittest

from pygiftparser import parser
from pygiftparser.gift import (
    MultipleChoiceCheckbox,
    MultipleChoiceRadio,
    TrueFalse,
    Short,
    Matching,
    Numerical,
    Range,
    MultipleNumerical,
    Essay,
    Description
)


class TestAllQuestions(unittest.TestCase):
    QUESTIONS_DESC = [
        {'type': MultipleChoiceRadio, 'num_options': 5},
        {'type': MultipleChoiceCheckbox, 'num_options': 4},
        {'type': TrueFalse, 'num_options': 1},
        {'type': TrueFalse, 'num_options': 1},
        {'type': TrueFalse, 'num_options': 1},
        {'type': TrueFalse, 'num_options': 1},
        {'type': Short, 'num_options': 3},
        {'type': Short, 'num_options': 2},
        {'type': Matching, 'num_options': 4},
        {'type': MultipleChoiceRadio, 'num_options': 3},
        {'type': MultipleChoiceRadio, 'num_options': 3},
        {'type': MultipleChoiceRadio, 'num_options': 4},
        {'type': Numerical, 'num_options': 1},
        {'type': Numerical, 'num_options': 1},
        {'type': Range, 'num_options': 1},
        {'type': MultipleNumerical, 'num_options': 2},
        {'type': MultipleNumerical, 'num_options': 2},
        {'type': Essay, 'num_options': 0},
        {'type': Description, 'num_options': 0}
    ]

    def setUp(self):
        with open('tests/gift_file_all_questions.txt', 'r') as myfile:
            s = myfile.read()
            self.result = parser.parse(s)
            self.questions = self.result.questions


    def tearDown(self):
        self.result.questions = []
        self.result = None


    def test_number_of_questions(self):
        self.assertEqual(len(self.result.questions), 19)


    def _test_question(self, answer, type_a, num_options):
        self.assertTrue(isinstance(answer, type_a))
        self.assertEqual(len(answer.options), num_options)


    def test_all_answers(self):
        for i in range(19):
            self._test_question(
                self.questions[i].answer,
                self.QUESTIONS_DESC[i]['type'],
                self.QUESTIONS_DESC[i]['num_options'],
            )
