import unittest

from pygiftparser import parser


class TestAllExampleFiles(unittest.TestCase):
    FILES_DESC = [
        {"file_name": "tests/gift_file_all_questions.txt", "number_of_questions": 19},
        {"file_name": "tests/gift_file_categories.txt", "number_of_questions": 19},
        {"file_name": "example_files/test1.txt", "number_of_questions": 4},
        {"file_name": "example_files/test10.txt", "number_of_questions": 10},
        {"file_name": "example_files/test11.txt", "number_of_questions": 4},
        {"file_name": "example_files/test12.txt", "number_of_questions": 19},
        {"file_name": "example_files/test2.txt", "number_of_questions": 7},
        {"file_name": "example_files/test3.txt", "number_of_questions": 7},
        {"file_name": "example_files/test4.txt", "number_of_questions": 30},
        {"file_name": "example_files/test5.txt", "number_of_questions": 40},
        {"file_name": "example_files/test6.txt", "number_of_questions": 5},
        {"file_name": "example_files/test7.txt", "number_of_questions": 7},
        {"file_name": "example_files/test8.txt", "number_of_questions": 5},
        {"file_name": "example_files/test9.txt", "number_of_questions": 19},
    ]

    def setUp(self):
        self.result = []
        self.num_questions = []
        for i in range(14):
            with open(self.FILES_DESC[i]['file_name']) as myfile:
                s = myfile.read()
                parsed_file = parser.parse(s)
                self.result.append(parsed_file)
                self.num_questions.append(len(parsed_file.questions))


    def tearDown(self):
        self.result = []
        self.num_questions = []


    def _test_file(self, file_name, given_number_questions, correct_number_questions):
        self.assertEqual(given_number_questions, correct_number_questions, msg=file_name)


    def test_all_files(self):
        for i in range(14):
            self._test_file(
                self.FILES_DESC[i]['file_name'],
                self.num_questions[i],
                self.FILES_DESC[i]['number_of_questions'],
            )
