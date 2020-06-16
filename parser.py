import argparse
import re
from ply import lex
import ply.yacc as yacc

import preprocessor
import gift


gift_result = gift.Gift()


# Lex #########################################################################

# List of token names.
tokens = (
    'COLONCOLON',
    'OPEN_BRACE',
    'CLOSE_BRACE',
    'NEWLINE',
    'CHAR',
    'STRING'
)

# Regular expression rules for simple tokens.
t_COLONCOLON  = r'::'
t_OPEN_BRACE  = r'{'
t_CLOSE_BRACE = r'}'
t_CHAR        = r'[^\{\}\n]' # everything but open/close brace and newline.
def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.lexer.linestart = t.lexer.lexpos

# Error.
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()


# Yacc ########################################################################

def p_expression_goal(p):
    'goal : gift'
    p[0] = p[1]


def p_expression_gift(p):
    """
    gift : question_type
    gift : gift NEWLINE NEWLINE question_type
    """
    p[0] = gift_result


def p_expression_question_type(p):
    """
    question_type : OPEN_BRACE OPEN_BRACE string CLOSE_BRACE CLOSE_BRACE question
    question_type : question
    """
    if len(p) == 2:
        question = gift_result.questions[-1]
        question.name = question.text
    elif len(p) == 7:
        question = gift_result.questions[-1]
        question.name = p[3].strip()


def p_expression_question(p):
    'question : string brace_expr'
    question = gift_result.questions[-1]
    question.text = p[1].strip()


def p_expression_brace_expr(p):
    """
    brace_expr :
    brace_expr : OPEN_BRACE CLOSE_BRACE
    brace_expr : OPEN_BRACE answer CLOSE_BRACE question_continue
    """
    question = gift.Question()

    if len(p) == 1:
        question.answer = gift.AnswerFactory.build('')
    elif len(p) == 3:
        question.answer = gift.AnswerFactory.build('{}')
    elif len(p) == 5:
        question.answer = gift.AnswerFactory.build(p[2])
        if p[4]:
            question.text_continue = p[4]

    gift_result.add(question)


def p_expression_question_continue(p):
    """
    question_continue :
    question_continue : string
    """
    if len(p) == 1:
        p[0] = ''
    elif len(p) == 2:
        p[0] = p[1].strip()


def p_expression_answer(p):
    'answer : string'
    p[0] = p[1].strip()


def p_expression_string(p):
    """
    string : string CHAR
    string : CHAR
    """
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1] + p[2]


# Error rule for syntax errors
def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' in line {p.lineno}. " + str(p))
        raise Exception(f"Syntax error at '{p.value}' in line {p.lineno}.")
    else:
        print('Syntax error at EOI')
        raise Exception('Syntax error at EOI: ')


parser = yacc.yacc()


def parse(s):
    res = preprocessor.preprocess(s)
    return parser.parse(res)