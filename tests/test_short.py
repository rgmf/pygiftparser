import unittest

from pygiftparser import parser
from pygiftparser.gift import Short


class TestShortQuestion(unittest.TestCase):
    def setUp(self):
        self.result = parser.parse('Question number 1 {=answer 1 =answer 2}')


    def tearDown(self):
        self.result.questions = []
        self.result = None


    def test_short_question(self):        
        self.assertEqual(len(self.result.questions), 1)

        question = self.result.questions[0]
        self.assertEqual(question.name, 'Question number 1')
        self.assertEqual(question.text, 'Question number 1')
        self.assertEqual(question.text_continue, None)

        answer = question.answer
        self.assertTrue(isinstance(answer, Short))
        self.assertEqual(len(answer.options), 2)

        opt = answer.options[0]
        self.assertEqual(opt.prefix, '=')
        self.assertEqual(opt.text, 'answer 1')
        self.assertEqual(opt.percentage, 1.0)
        self.assertEqual(opt.raw_text, '=answer 1')
        self.assertEqual(opt.feedback, None)

        opt = answer.options[1]
        self.assertEqual(opt.prefix, '=')
        self.assertEqual(opt.text, 'answer 2')
        self.assertEqual(opt.percentage, 1.0)
        self.assertEqual(opt.raw_text, '=answer 2')
        self.assertEqual(opt.feedback, None)


class TestShortQuestionWithName(unittest.TestCase):
    def setUp(self):
        self.result = parser.parse('::Name 1::Question number 1 {=answer 1 =answer 2}')


    def tearDown(self):
        self.result.questions = []
        self.result = None


    def test_short_question(self):        
        self.assertEqual(len(self.result.questions), 1)

        question = self.result.questions[0]
        self.assertEqual(question.name, 'Name 1')
        self.assertEqual(question.text, 'Question number 1')
        self.assertEqual(question.text_continue, None)

        answer = question.answer
        self.assertTrue(isinstance(answer, Short))
        self.assertEqual(len(answer.options), 2)

        opt = answer.options[0]
        self.assertEqual(opt.prefix, '=')
        self.assertEqual(opt.text, 'answer 1')
        self.assertEqual(opt.percentage, 1.0)
        self.assertEqual(opt.raw_text, '=answer 1')
        self.assertEqual(opt.feedback, None)

        opt = answer.options[1]
        self.assertEqual(opt.prefix, '=')
        self.assertEqual(opt.text, 'answer 2')
        self.assertEqual(opt.percentage, 1.0)
        self.assertEqual(opt.raw_text, '=answer 2')
        self.assertEqual(opt.feedback, None)


class TestShortNQuestions(unittest.TestCase):
    def setUp(self):
        self.result = parser.parse("""
            ::Name 1::Question number 1       {=answer 1 =answer 2}
            \n
            \n
                Question number 2 { =4\=four =four\=4 }
        """)


    def tearDown(self):
        self.result.questions = []
        self.result = None


    def test_short_question(self):        
        self.assertEqual(len(self.result.questions), 2)

        question1 = self.result.questions[0]
        question2 = self.result.questions[1]
        self.assertEqual(question1.name, 'Name 1')
        self.assertEqual(question2.name, 'Question number 2')
        self.assertEqual(question1.text, 'Question number 1')
        self.assertEqual(question2.text, 'Question number 2')
        self.assertEqual(question1.text_continue, None)
        self.assertEqual(question2.text_continue, None)

        answer1 = question1.answer
        answer2 = question2.answer
        self.assertTrue(isinstance(answer1, Short))
        self.assertTrue(isinstance(answer2, Short))
        self.assertEqual(len(answer1.options), 2)
        self.assertEqual(len(answer2.options), 2)

        opt = answer1.options[0]
        self.assertEqual(opt.prefix, '=')
        self.assertEqual(opt.text, 'answer 1')
        self.assertEqual(opt.percentage, 1.0)
        self.assertEqual(opt.raw_text, '=answer 1')
        self.assertEqual(opt.feedback, None)

        opt = answer1.options[1]
        self.assertEqual(opt.prefix, '=')
        self.assertEqual(opt.text, 'answer 2')
        self.assertEqual(opt.percentage, 1.0)
        self.assertEqual(opt.raw_text, '=answer 2')
        self.assertEqual(opt.feedback, None)

        opt = answer2.options[0]
        self.assertEqual(opt.prefix, '=')
        self.assertEqual(opt.text, '4\\=four')
        self.assertEqual(opt.percentage, 1.0)
        self.assertEqual(opt.raw_text, '=4\\=four')
        self.assertEqual(opt.feedback, None)

        opt = answer2.options[1]
        self.assertEqual(opt.prefix, '=')
        self.assertEqual(opt.text, 'four\\=4')
        self.assertEqual(opt.percentage, 1.0)
        self.assertEqual(opt.raw_text, '=four\\=4')
        self.assertEqual(opt.feedback, None)


class TestShortQuestionWithContinue(unittest.TestCase):
    def setUp(self):
        self.result = parser.parse('Question number 1 {=answer 1 =answer 2} continue text.')


    def tearDown(self):
        self.result.questions = []
        self.result = None


    def test_short_question(self):        
        self.assertEqual(len(self.result.questions), 1)

        question = self.result.questions[0]
        self.assertEqual(question.name, 'Question number 1')
        self.assertEqual(question.text, 'Question number 1')
        self.assertEqual(question.text_continue, 'continue text.')

        answer = question.answer
        self.assertTrue(isinstance(answer, Short))
        self.assertEqual(len(answer.options), 2)

        opt = answer.options[0]
        self.assertEqual(opt.prefix, '=')
        self.assertEqual(opt.text, 'answer 1')
        self.assertEqual(opt.percentage, 1.0)
        self.assertEqual(opt.raw_text, '=answer 1')
        self.assertEqual(opt.feedback, None)

        opt = answer.options[1]
        self.assertEqual(opt.prefix, '=')
        self.assertEqual(opt.text, 'answer 2')
        self.assertEqual(opt.percentage, 1.0)
        self.assertEqual(opt.raw_text, '=answer 2')
        self.assertEqual(opt.feedback, None)


class TestShortQuestionWithContinueAndFeedback1(unittest.TestCase):
    def setUp(self):
        self.result = parser.parse('Question number 1 {=answer 1 =answer 2 # feedback 2} continue text.')


    def tearDown(self):
        self.result.questions = []
        self.result = None


    def test_short_question(self):        
        self.assertEqual(len(self.result.questions), 1)

        question = self.result.questions[0]
        self.assertEqual(question.name, 'Question number 1')
        self.assertEqual(question.text, 'Question number 1')
        self.assertEqual(question.text_continue, 'continue text.')

        answer = question.answer
        self.assertTrue(isinstance(answer, Short))
        self.assertEqual(len(answer.options), 2)

        opt = answer.options[0]
        self.assertEqual(opt.prefix, '=')
        self.assertEqual(opt.text, 'answer 1')
        self.assertEqual(opt.percentage, 1.0)
        self.assertEqual(opt.raw_text, '=answer 1')
        self.assertEqual(opt.feedback, None)

        opt = answer.options[1]
        self.assertEqual(opt.prefix, '=')
        self.assertEqual(opt.text, 'answer 2')
        self.assertEqual(opt.percentage, 1.0)
        self.assertEqual(opt.raw_text, '=answer 2')
        self.assertEqual(opt.feedback, 'feedback 2')


class TestShortQuestionWithContinueAndFeedback2(unittest.TestCase):
    def setUp(self):
        self.result = parser.parse('Question number 1 {=answer 1 # feedback 1 =answer 2 # feedback 2} continue text.')


    def tearDown(self):
        self.result.questions = []
        self.result = None


    def test_short_question(self):        
        self.assertEqual(len(self.result.questions), 1)

        question = self.result.questions[0]
        self.assertEqual(question.name, 'Question number 1')
        self.assertEqual(question.text, 'Question number 1')
        self.assertEqual(question.text_continue, 'continue text.')

        answer = question.answer
        self.assertTrue(isinstance(answer, Short))
        self.assertEqual(len(answer.options), 2)

        opt = answer.options[0]
        self.assertEqual(opt.prefix, '=')
        self.assertEqual(opt.text, 'answer 1')
        self.assertEqual(opt.percentage, 1.0)
        self.assertEqual(opt.raw_text, '=answer 1')
        self.assertEqual(opt.feedback, 'feedback 1')

        opt = answer.options[1]
        self.assertEqual(opt.prefix, '=')
        self.assertEqual(opt.text, 'answer 2')
        self.assertEqual(opt.percentage, 1.0)
        self.assertEqual(opt.raw_text, '=answer 2')
        self.assertEqual(opt.feedback, 'feedback 2')


class TestShortQuestionWithContinue2(unittest.TestCase):
    def setUp(self):
        self.result = parser.parse('::With name::Question number 1 {=answer 1 =answer 2} with continue text.')
        self.question = self.result.questions[0]
        self.answer = self.question.answer
        self.options = self.answer.options


    def tearDown(self):
        self.result.questions = []
        self.result = None


    def test_name_and_text_of_questions(self):
        self.assertEqual(self.question.name, "With name")
        self.assertEqual(self.question.text, "Question number 1")
        self.assertEqual(self.question.text_continue, 'with continue text.')


class TestShortQuestionError(unittest.TestCase):
    def test_error_not_closed_bracket(self):
        with self.assertRaises(Exception):
            self.result = parser.parse('::Name 1::Question number 1 {=answer 1 =answer 2')


    def test_error_not_opened_bracket(self):
        with self.assertRaises(Exception):
            self.result = parser.parse('::Name 1::Question number 1 =answer 1 =answer 2}')
