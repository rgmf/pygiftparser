import re
from abc import ABC, abstractmethod


class Gift:
    def __init__(self):
        self.questions = []

    def add(self, q):
        self.questions.append(q)


class Question:
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name', None)
        self.text = kwargs.get('text', None)
        self.text_continue = kwargs.get('text_continue', None)
        self.answer = kwargs.get('answer', None)


    def is_missing_word(self):
        return bool(self.text and self.text_continue)


class AnswerFactory(object):
    @classmethod
    def build(cls, raw_answer):
        """
        Builds the answer from the raw_answer.

        :str raw_answer: the string between braces in GIFT files.
        :ret:            returns the answer
        """
        options = AnswerFactory._build_options(raw_answer)
        if TrueFalse.is_answer(options):
            return TrueFalse(options, raw_answer=raw_answer)

        if Matching.is_answer(options):
            return Matching(options, raw_answer=raw_answer)
        
        if Short.is_answer(options):
            return Short(options, raw_answer=raw_answer)

        if Numerical.is_answer(options):
            return Numerical(options, raw_answer=raw_answer)

        if NumericalMultiple.is_answer(options):
            return NumericalMultiple(options, raw_answer=raw_answer)

        if NumericalRange.is_answer(options):
            return NumericalRange(options, raw_answer=raw_answer)

        if MultipleChoiceRadio.is_answer(options):
            return MultipleChoiceRadio(options, raw_answer=raw_answer)

        if MultipleChoiceCheckbox.is_answer(options):
            return MultipleChoiceCheckbox(options, raw_answer=raw_answer)

        if Essay.is_answer(options):
            return Essay(options, raw_answer=raw_answer)

        if Description.is_answer(options):
            return Description(options, raw_answer=raw_answer)

        raise Exception('AnswerFactory.build: Syntax error: malformed answer: "' + raw_answer.strip() + '"')


    @classmethod
    def _build_options(self, raw_answer):
        """
        Builds an array with every option in the raw_answer.

        Every option in the array will include '=' and '~' if option contains
        them.

        For example: '=response 1 ~response 2 ~response 3' results in an array
        like this: ['=response 1', '~response 2', '~response 3'].

        Another example: 'TRUE' results in an array like this: ['TRUE'].

        :str raw_answer: string between braces in GIFT file.
        :ret:            returns an array with all options in the raw_answer.
                         The array can be empty.
        """
        raw_answer = raw_answer.strip()
        if len(raw_answer) == 0:
            return []

        pattern = re.compile(r'^[=~]{1}|[^\\][=~]{1}')
        n = len(re.findall(pattern, raw_answer))
        if (raw_answer[0] != '=' and raw_answer[0] != '~'):
            if n > 0 and raw_answer[0] != '#':
                raise Exception('AnswerFactory._build_options: Syntax error: malformed answer: "' + raw_answer + '"')
            return [raw_answer]
        else:
            prev = None
            options = []
            option = raw_answer[0]
            for c in raw_answer[1:]:
                if (c == '=' or c =='~') and prev != '\\':
                    options.append(option)
                    option = c
                else:
                    option = option + c
                prev = c
            options.append(option)
            return options


class Answer(ABC):

    def __init__(self, options: list, *args, **kwargs):
        # Raw answer like was in gift file between braces.
        self.raw_answer = kwargs.get('raw_answer', None)

        # Catch feedback from every answer (can be None).
        self.feedback = []
        for idx, val in enumerate(options):
            pos = val.find('#')
            if pos > 0 and val[pos - 1] != '\\':
                self.feedback.append(val[pos + 1:].strip())
                options[idx] = options[idx][:pos].strip()
            else:
                self.feedback.append(None)


    @staticmethod
    @abstractmethod
    def is_answer(options: list) -> bool:
        pass


    @staticmethod
    @abstractmethod
    def get_pattern() -> re.Pattern:
        pass


class Essay(Answer):
    PATTERN = re.compile(r'^\{\}$')

    def __init__(self, options: list, *args, **kwargs):
        super().__init__(options, options, *args, **kwargs)
        self.answer = ''


    def __repr__(self):
        return 'Essay()'


    def __str__(self):
        return '(Essay answer)'


    @staticmethod
    def is_answer(options: list) -> bool:
        return len(options) == 1 and Essay.PATTERN.match(options[0])


    @staticmethod
    def get_pattern() -> re.Pattern:
        return Essay.PATTERN


class Description(Answer):
    PATTERN = re.compile(r'^$')

    def __init__(self, options: list, *args, **kwargs):
        super().__init__(options, options, *args, **kwargs)
        self.answer = ''


    def __repr__(self):
        return 'Description()'


    def __str__(self):
        return '(Description answer)'


    @staticmethod
    def is_answer(options: list) -> bool:
        return len(options) == 0


    @staticmethod
    def get_pattern() -> re.Pattern:
        return Description.PATTERN


class TrueFalse(Answer):
    PATTERN = re.compile(r'^TRUE(#.+){0,1}$|^FALSE(#.+){0,1}$|^T(#.+){0,1}$|^F(#.+){0,1}$|^true(#.+){0,1}$|^false(#.+){0,1}$|^t(#.+){0,1}$|^f(#.+){0,1}$')
    TRUE_PATTERN = re.compile(r'^TRUE$|^T$|^true$|^t$')
    FALSE_PATTERN = re.compile(r'^FALSE$|^F$|^false$|^f$')

    def __init__(self, options: list, *args, **kwargs):
        super().__init__(options, *args, **kwargs)

        # True-False answers can have two feedback. It looks for the second 
        # one in the current feedback text.
        if len(self.feedback) == 1 and self.feedback[0]:
            pos = self.feedback[0].find('#')
            val = self.feedback[0]
            if pos > 0 and val[pos - 1] != '\\':
                self.feedback.append(val[pos + 1:].strip())
                self.feedback[0] = val[:pos].strip()

        # The answer can be True or False.
        self.answer = False
        if self.TRUE_PATTERN.match(options[0]):
            self.answer = True


    def __repr__(self):
        return 'TrueFalse()'


    def __str__(self):
        return str(self.answer)


    @staticmethod
    def is_answer(options: list) -> bool:
        if len(options) == 1 and TrueFalse.PATTERN.match(options[0]):
            return True
        else:
            return False


    @staticmethod
    def get_pattern() -> re.Pattern:
        return TrueFalse.PATTERN


class MultipleChoiceRadio(Answer):
    PATTERN = re.compile(r'^=(%[0-9]+%){0,1}(.+)$|^~.+$')
    VALID_PATTERN = re.compile(r'^=(%[0-9]+%){0,1}(.+)$')
    ERROR_PATTERN = re.compile(r'^~.+$')

    def __init__(self, options, *args, **kwargs):
        """
        :array options: array with all options.
        """
        super().__init__(options, *args, **kwargs)
        self.answer = list(
            map(lambda opt: 
                {
                    'text': opt[1:].strip(),
                    'percentage': 1 if opt[0] == '=' else 0
                },
                options
            )
        )


    def __repr__(self):
        return 'MultipleChoiceRadio()'


    def __str__(self):
        a = [ i['text'] + ' (' + str(i['percentage'] * 100) + '%)' for i in self.answer ]
        return '\n'.join(a)


    @staticmethod
    def is_answer(options: list) -> bool:
        total = len(options)
        valid = len(list(filter(lambda x: MultipleChoiceRadio.VALID_PATTERN.match(x), options)))
        error = len(list(filter(lambda x: MultipleChoiceRadio.ERROR_PATTERN.match(x), options)))
        return total > 0 and total == (valid + error) and valid == 1


    @staticmethod
    def get_pattern() -> re.Pattern:
        return MultipleChoiceRadio.PATTERN


class MultipleChoiceCheckbox(Answer):
    PATTERN = re.compile(r'^~(%(-{0,1}[0-9]+)%)(.+)$')

    def __init__(self, options, *args, **kwargs):
        """
        :array options: array with all options.
        """
        super().__init__(options, *args, **kwargs)
        self.answer = list(
            map(lambda opt: 
                {
                    'text': self.PATTERN.match(opt).group(3),
                    'percentage': int(self.PATTERN.match(opt).group(2)) / 100
                },
                options
            )
        )


    def __repr__(self):
        return 'MultipleChoiceCheckbox()'


    def __str__(self):
        a = [ i['text'] + '(' + str(i['percentage'] * 100) + '%)' for i in self.answer ]
        return '\n'.join(a)


    @staticmethod
    def is_answer(options: list) -> bool:
        total = len(options)
        count = len(list(filter(lambda x: MultipleChoiceCheckbox.PATTERN.match(x), options)))
        return total > 0 and total == count


    @staticmethod
    def get_pattern() -> re.Pattern:
        return MultipleChoiceCheckbox.PATTERN


class Short(Answer):
    PATTERN = re.compile(r'^=(%([0-9]+)%){0,1}(.+)$')

    def __init__(self, options, *args, **kwargs):
        """
        :array options: array with all valid options.
        """
        super().__init__(options, *args, **kwargs)
        self.answer = []

        # Extract first character for all options (the '=').
        for opt in options:
            match = self.PATTERN.match(opt)
            if match.group(1):
                percentage = int(match.group(2)) / 100
                text = match.group(3)
            else:
                percentage = 1.0
                text = match.group(3)
            self.answer.append({'text': text, 'percentage': percentage})


    def __repr__(self):
        return 'Short()'


    def __str__(self):
        a = [ i['text'] + '(' + str(i['percentage'] * 100) + '%)' for i in self.answer ]
        return '\n'.join(a)


    @staticmethod
    def is_answer(options: list) -> bool:
        total = len(options)
        count = len(list(filter(lambda x: Short.PATTERN.match(x), options)))
        return total > 0 and total == count


    @staticmethod
    def get_pattern(options: list) -> bool:
        return Short.PATTERN


class Numerical(Answer):
    PATTERN = re.compile(r'^#([0-9]+(\.[0-9]+){0,1})((:([0-9]+(\.[0-9]+){0,1})){0,1})$')

    def __init__(self, options: list, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self.answer = {}
        match = self.PATTERN.match(options[0])
        if match.group(3):
            number = float(match.group(1))
            error = float(match.group(5))
        else:
            number = float(match.group(1))
            error = 0.0
        self.answer = {'number': number, 'error': error}


    def __repr__(self):
        return 'Numerical()'


    def __str__(self):
        return str(self.answer['number']) + ' (+-' + str(self.answer['error']) + ')'


    @staticmethod
    def is_answer(options: list) -> bool:
        return len(options) == 1 and Numerical.PATTERN.match(options[0])


    @staticmethod
    def get_pattern() -> re.Pattern:
        return Numerical.PATTERN


class NumericalMultiple(Answer):
    NUM_PATTERN              = re.compile(r'^=([0-9]+(\.[0-9]+){0,1})((:([0-9]+(\.[0-9]+){0,1})){0,1})$')
    NUM_PERCENTAGE_PATTERN   = re.compile(r'^=(%([0-9]+)%){1}([0-9]+(\.[0-9]+){0,1})((:([0-9]+(\.[0-9]+){0,1})){0,1})$')
    RANGE_PATTERN            = re.compile(r'^=([0-9]+(\.[0-9]+){0,1})\.\.([0-9]+(\.[0-9]+){0,1})')
    RANGE_PERCENTAGE_PATTERN = re.compile(r'^=(%([0-9]+)%){1}([0-9]+(\.[0-9]+){0,1})\.\.([0-9]+(\.[0-9]+){0,1})')
    PATTERN = re.compile(r'^=([0-9]+(\.[0-9]+){0,1})((:([0-9]+(\.[0-9]+){0,1})){0,1})$|^=(%([0-9]+)%){1}([0-9]+(\.[0-9]+){0,1})((:([0-9]+(\.[0-9]+){0,1})){0,1})$|^=([0-9]+(\.[0-9]+){0,1})\.\.([0-9]+(\.[0-9]+){0,1})|^=(%([0-9]+)%){1}([0-9]+(\.[0-9]+){0,1})\.\.([0-9]+(\.[0-9]+){0,1})')

    MODE_NUM = 'mode-num'
    MODE_RANGE = 'mode-range'

    def __init__(self, options: list, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self.answer = []
        num_options = NumericalMultiple.build_options(options[0]) if len(options) == 1 else []
        for i in num_options:
            if self.NUM_PATTERN.match(i):
                match = self.NUM_PATTERN.match(i)
                a = {
                    'mode': self.MODE_NUM,
                    'number': float(match.group(1)),
                    'error': float(match.group(5)),
                    'percentage': 1
                }
            elif self.NUM_PERCENTAGE_PATTERN.match(i):
                match = self.NUM_PERCENTAGE_PATTERN.match(i)
                a = {
                    'mode': self.MODE_NUM,
                    'number': float(match.group(3)),
                    'error': float(match.group(7)),
                    'percentage': float(match.group(2)) / 100
                }
            elif self.RANGE_PATTERN.match(i):
                match = self.RANGE_PATTERN.match(i)
                a = {
                    'mode': self.MODE_RANGE,
                    'from': float(match.group(1)),
                    'to': float(match.group(3)),
                    'percentage': 1
                }
            elif self.RANGE_PERCENTAGE_PATTERN.match(i):
                match = self.RANGE_PERCENTAGE_PATTERN.match(i)
                a = {
                    'mode': self.MODE_RANGE,
                    'from': float(match.group(3)),
                    'to': float(match.group(5)),
                    'percentage': float(match.group(2)) / 100
                }
            else:
                raise Exception('NumericalMultiple.__init__: syntax error: answer number: ' + i + ' not valid')

            self.answer.append(a)


    def __repr__(self):
        return 'NumericalMultiple()'


    def __str__(self):
        return '\n'.join([ str(numerical) for numerical in self.answer ])


    @staticmethod
    def build_options(answer: str) -> bool:
        if answer[0] == '#':
            answer = answer[1:].strip()
            if answer[0] == '=':
                res = [ '=' + a.strip() for a in answer.split('=')[1:] ]
                return res
        return []


    @staticmethod
    def is_answer(options: list) -> bool:
        if len(options) == 1:
            num_options = NumericalMultiple.build_options(options[0])
            total = len(num_options)
            count = len(list(filter(lambda x: NumericalMultiple.PATTERN.match(x), num_options)))
            return total > 1 and total == count
        return False


    @staticmethod
    def get_pattern() -> re.Pattern:
        return NumericalMultiple.PATTERN


class NumericalRange(Answer):
    PATTERN = re.compile(r'^#([0-9]+(\.[0-9]+){0,1})\.\.([0-9]+(\.[0-9]+){0,1})')

    def __init__(self, options: list, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        match = self.PATTERN.match(options[0])
        self.answer = {'from': match.group(1), 'to': match.group(3)}


    def __repr__(self):
        return 'NumericalRange()'


    def __str__(self):
        return self.answer['from'] + ' .. ' + self.answer['to']


    @staticmethod
    def is_answer(options: list) -> bool:
        return len(options) == 1 and NumericalRange.PATTERN.match(options[0])


    @staticmethod
    def get_pattern() -> re.Pattern:
        return NumericaRange.PATTERN


class Matching(Answer):
    PATTERN = re.compile(r'^=(.+)->(.+$)')

    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self.answer = []
        for opt in options:
            match = self.PATTERN.match(opt)
            self.answer.append({
                'pair1': match.group(1).strip(),
                'pair2': match.group(2).strip()
            })


    def __repr__(self):
        return 'Matching()'


    def __str__(self):
        a = [ i['pair1'] + ' -> ' + i['pair2'] for i in self.answer ]
        return '\n'.join(a)


    @staticmethod
    def is_answer(options: list) -> bool:
        total = len(options)
        count = len(list(filter(lambda x: Matching.PATTERN.match(x), options)))
        return total >= 3 and total == count


    @staticmethod
    def get_pattern() -> re.Pattern:
        return Numerical.PATTERN
