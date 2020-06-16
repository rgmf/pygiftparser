class Gift:
    questions = []

    def add(self, q):
        self.questions.append(q)


class Question:
    name = None
    text = None
    answer = None


class Answer:
    correct_answers = []


class Essay(Answer):
    answer = None


class Description(Answer):
    answer = None


class TrueFalse(Answer):
    answer = None


class MultipleChoice(Answer):
    options = []


class Short(Answer):
    answer = None


class Numerical(Answer):
    answer = None
    error = None


class Matching(Answer):
    pairs = []


class MissingWord(Answer):
    options = []
