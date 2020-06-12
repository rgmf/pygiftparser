import re


TYPE_MULTIPLE_CHOICE = 'multiple-choice'
TYPE_TRUE_FALSE = 'true-false'
TYPE_SHORT = 'short'
TYPE_MATCHING = 'matching'
TYPE_MISSING_WORD = 'missing-word'
TYPE_NUMERICAL = 'numerical'
TYPE_ESSAY = 'essay'
TYPE_DESCRIPTION = 'description'


def build_true_false_answer(match):
    return {
        'type': TYPE_TRUE_FALSE,
        'answer': match.string,
        'percentage': '100'
    }


def build_multiple_or_short_answer(match):
    string = match.string
    prefix = string[0]
    percentage = match.group(1)[1:-1]
    answer = match.group(2)

    if prefix == '=' and re.match(r'^%[0-9]+%', string[1:]):
        type_answer = TYPE_SHORT
    else:
        type_answer = TYPE_MULTIPLE_CHOICE

    return {
        'type': type_answer,
        'answer': answer,
        'percentage': percentage
    }


def build_short_answer(match):
    return {
        'type': [TYPE_SHORT, TYPE_MULTIPLE_CHOICE],
        'answer': match.string[1:]
    }


def build_multiple_choice_answer(match):
    return {
        'type': TYPE_MULTIPLE_CHOICE,
        'answer': match.string[1:],
        'percentage': '100' if match.string[1] == '=' else '0'
    }


def build_numerical_answer(match):
    return {
        'type': TYPE_NUMERICAL,
        'answer': match.group(1),
        'error': match.group(3)
    }


def create_answer(answer):
    true_false_pattern = re.compile('^TRUE$|^FALSE$|^T$|^F$|^true$|^false$|^t$|^f$')
    multiple_or_short_patter = re.compile('^[=~](%[0-9]+%)(.+)$')
    short_patter = re.compile('^=.+$')
    multiple_choice_patter = re.compile('^~.+$')
    numerical_pattern = re.compile('^#([0-9]+(\.[0-9]+){0,1})((:[0-9]+(\.[0-9]+){0,1}){0,1})$')

    match = true_false_pattern.match(answer)
    if match:
        return build_true_false_answer(match)

    match = multiple_or_short_patter.match(answer)
    if match:
        return build_multiple_or_short_answer(match)

    match = short_patter.match(answer)
    if match:
        return build_short_answer(match)

    match = multiple_choice_patter.match(answer)
    if match:
        return build_multiple_choice_answer(match)

    match = numerical_pattern.match(answer)
    if match:
        return build_numerical_answer(match)
        
    return None