import functools
import re
from abc import ABC, abstractmethod


class Gift:
    def __init__(self):
        self.questions = []

    def add(self, q):
        self.questions.append(q)


class SemanticError(Exception):
    pass


class QuestionFactory(object):
    @classmethod
    def build(cls, raw_text, answer, text_continue):
        """
        Builds a Question object splitting name and text parts if needed.
        """
        p = re.compile(r'^::(.+)::(.+)$')
        m = p.match(raw_text)
        name = m.group(1).strip() if m and m.group(1) else raw_text
        text = m.group(2).strip() if m and m.group(2) else raw_text
        return Question(
            name=name, text=text, answer=answer, text_continue=text_continue
        )


class AnswerFactory(object):
    @classmethod
    def build(cls, options: list):
        """
        Builds the answer from the options

        :list options: the options.
        :ret:          returns the answer.
        """
        if options == None:
            return Description()

        if TrueFalse.is_answer(options):
            return TrueFalse(options=options)
        
        if Matching.is_answer(options):
            return Matching(options=options)
        
        if Short.is_answer(options):
            return Short(options=options)

        if Numerical.is_answer(options):
            return Numerical(options=options)

        if MultipleChoiceRadio.is_answer(options):
            return MultipleChoiceRadio(options=options)

        if MultipleChoiceCheckbox.is_answer(options):
            return MultipleChoiceCheckbox(options=options)

        if Essay.is_answer(options):
            return Essay(options=options)

        raise SemanticError(
                'AnswerFactory.build: Semantic error in the options: "' + \
                ', '.join(list(map(lambda o: o.raw_text, options))) + '"')


class Question:
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name', None)
        self.text = kwargs.get('text', None)
        self.text_continue = kwargs.get('text_continue', None)
        self.answer = kwargs.get('answer', None)


    def is_missing_word(self):
        return bool(self.text and self.text_continue)


    def __str__(self):
        res = 'Question: '
        if self.name:
            res = res + self.name
        res = res + '\n' + 'Text: ' + self.text + ('_______' + self.text_continue if self.text_continue else '')
        res = res + '\n' + 'Type answer: ' + self.answer.__repr__()
        res = res + '\n' + str(self.answer) + '\n'
        return res


class Answer(ABC):
    def __init__(self, *args, **kwargs):
        self.options = kwargs.get('options', [])


    def __str__(self):
        if len(self.options) > 1:
            return 'Answer:\n' + functools.reduce(
                lambda x, y: str(x) + '\n' + str(y), self.options
            )
        elif len(self.options) == 1:
            return 'Answer:\n' + str(self.options[0])
        else:
            return 'Answer:\n(No options)'


    @staticmethod
    @abstractmethod
    def is_answer(options: list) -> bool:
        pass


class Option:
    def __init__(self, *args, **kwargs):
        self.feedback = kwargs.get('feedback', None)
        self.raw_text = kwargs.get('text', None)
        self.prefix, self.text, self.percentage = self._extract_parts(self.raw_text)


    def _extract_parts(self, raw_text):
        if raw_text:
            pattern = re.compile(r'^[#=~](%(-{0,1}[0-9]+)%)?(.+)$')
            match = pattern.match(raw_text)
            if match:
                prefix = raw_text[0]
                text = match.group(3)
                if match.group(2):
                    percentage = int(match.group(2))/100
                elif prefix == '=' or prefix == '#':
                    percentage  = 1.0
                else:
                    percentage = 0.0
                return prefix, text, percentage
            else:
                return None, raw_text, 1.0
        return None, None, None


    def __str__(self):
        if self.feedback:
            res = 'Option: ' + self.text + ' [' + str(self.percentage) + ']' \
                + ' (' + self.feedback + ')'
        else:
            res = 'Option: ' + self.text + ' [' + str(self.percentage) + ']'
        res = '(' + self.prefix + ') ' + res if self.prefix else res
        return res


class TrueFalse(Answer):
    def __repr__(self):
        return 'TrueFalse()'


    @staticmethod
    def is_answer(options: list) -> bool:
        return len(options) == 1 and options[0].text in ['True', 'False']


class Matching(Answer):
    PATTERN = re.compile(r'^(.+)->(.+$)')

    def __repr__(self):
        return 'Matching()'


    def get_pair(self, option: Option) -> dict:
        match = self.PATTERN.match(option.text)
        if match:
            return({
                'pair1': match.group(1).strip(),
                'pair2': match.group(2).strip()
            })
        else:
            return {'pair1': None, 'pair2': None}


    @staticmethod
    def is_answer(options: list) -> bool:
        total = len(options)
        count = len(list(filter(
            lambda opt: Matching.PATTERN.match(opt.text) and opt.prefix == '=', options))
        )
        return total >= 3 and total == count


class Short(Answer):
    def __repr__(self):
        return 'Short()'


    @staticmethod
    def is_answer(options: list) -> bool:
        total = len(options)
        count = len(list(filter(
            lambda opt: opt.prefix == '=', options))
        )
        return total > 0 and total == count


class Numerical(Answer):
    def __repr__(self):
        return 'Numerical()'


    @staticmethod
    def is_answer(options: list) -> bool:
        total = len(options)
        count = len(list(filter(
            lambda opt: opt.prefix == '#', options))
        )
        return total > 0 and total == count


class MultipleChoiceRadio(Answer):
    def __repr__(self):
        return 'MultipleChoiceRadio()'


    @staticmethod
    def is_answer(options: list) -> bool:
        total = len(options)
        valid = len(list(filter(lambda opt: opt.prefix == '=', options)))
        error = len(list(filter(lambda opt: opt.prefix == '~', options)))
        return total > 0 and total == (valid + error) and valid == 1


class MultipleChoiceCheckbox(Answer):
    def __repr__(self):
        return 'MultipleChoiceCheckbox()'


    @staticmethod
    def is_answer(options: list) -> bool:
        total = len(options)
        count = len(list(filter(lambda opt: opt.prefix == '~', options)))
        return total > 0 and total == count


class Essay(Answer):
    def __repr__(self):
        return 'Essay()'


    @staticmethod
    def is_answer(options: list) -> bool:
        return len(options) == 0


class Description(Answer):
    def __repr__(self):
        return 'Description()'


    @staticmethod
    def is_answer(options: list) -> bool:
        return options == None