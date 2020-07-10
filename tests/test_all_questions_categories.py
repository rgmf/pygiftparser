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


class TestAllQuestionsWithCategories(unittest.TestCase):
    QUESTIONS_DESC = [
        {'type': MultipleChoiceRadio, 'num_options': 5, 'category': None},
        {'type': MultipleChoiceCheckbox, 'num_options': 4, 'category': None},
        {'type': TrueFalse, 'num_options': 1, 'category': None},
        {'type': TrueFalse, 'num_options': 1, 'category': None},
        {'type': TrueFalse, 'num_options': 1, 'category': 'TrueFalseCategory'},
        {'type': TrueFalse, 'num_options': 1, 'category': 'TrueFalseCategory'},
        {'type': Short, 'num_options': 3, 'category': 'ShortCategory'},
        {'type': Short, 'num_options': 2, 'category': 'ShortCategory'},
        {'type': Matching, 'num_options': 4, 'category': 'MatchingCategory'},
        {'type': MultipleChoiceRadio, 'num_options': 3, 'category': 'MissingCategory'},
        {'type': MultipleChoiceRadio, 'num_options': 3, 'category': 'MissingCategory'},
        {'type': MultipleChoiceRadio, 'num_options': 4, 'category': 'MissingCategory'},
        {'type': Numerical, 'num_options': 1, 'category': 'NumericalCategory'},
        {'type': Numerical, 'num_options': 1, 'category': 'NumericalCategory'},
        {'type': Range, 'num_options': 1, 'category': 'NumericalCategory'},
        {'type': MultipleNumerical, 'num_options': 2, 'category': 'NumericalCategory'},
        {'type': MultipleNumerical, 'num_options': 2, 'category': 'NumericalCategory'},
        {'type': Essay, 'num_options': 0, 'category': 'EssayDescriptionCategory'},
        {'type': Description, 'num_options': 0, 'category': 'EssayDescriptionCategory'}
    ]

    def setUp(self):
        with open('tests/gift_file_categories.txt', 'r') as myfile:
            s = myfile.read()
            self.result = parser.parse(s)
            self.questions = self.result.questions


    def tearDown(self):
        self.result.questions = []
        self.result = None


    def test_number_of_questions(self):
        self.assertEqual(len(self.result.questions), 19)


    def _test_question(self, question, type_a, num_options, category):
        self.assertTrue(isinstance(question.answer, type_a))
        self.assertEqual(len(question.answer.options), num_options)
        self.assertEqual(question.category, category)


    def test_all_answers(self):
        for i in range(19):
            self._test_question(
                self.questions[i],
                self.QUESTIONS_DESC[i]['type'],
                self.QUESTIONS_DESC[i]['num_options'],
                self.QUESTIONS_DESC[i]['category']
            )
