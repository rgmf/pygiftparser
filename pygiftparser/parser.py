import argparse
from ply import lex
import ply.yacc as yacc

from . import preprocessor
from . import gift


gift_result = gift.Gift()
category = None


# Lex #########################################################################

# List of token names.
tokens = (
    'QUESTION',
    'QUESTIOND',
    'QUESTIONC',
    'OPTION',
    'FEEDBACK',
    'TRUE',
    'FALSE',
    'NUMERICAL',
    'RANGE',
    'MNUMERICAL',
    'LBRACKET',
    'RBRACKET',
    'CATEGORY'
)

t_QUESTION   = r'([^\\{\\}]|\\.)+?(?={)'
t_QUESTIOND  = r'([^\\{\\}]|\\.)+?(?=\n)|([^\\{\\}]|\\.)+$'
t_QUESTIONC  = r'}.+(?=[\n])|}.+$'
t_OPTION     = r'[ \t]*[=~]([^\\=\\~\\\#\\{\\}]|\\.)+?(?=[\=~\#\}])'
t_FEEDBACK   = r'[ \t]*\#.*?(?=[\=~\}])'
t_TRUE       = r'[ \t]*\|TRUE[ \t]*'
t_FALSE      = r'[ \t]*\|FALSE[ \t]*'
t_NUMERICAL  = r'[ \t]*\#[+-]?((\d+(\.\d*)?)|(\.\d+))(:[+-]?((\d+(\.\d*)?)|(\.\d+)))?[ \t]*(?=[\#\}])'
t_RANGE      = r'[ \t]*\#[+-]?\d+(\.\d+)?(:\d+(\.\d+)?)?\.\.[+-]?\d+(\.\d+)?(:\d+(\.\d+)?)?[ \t]*(?=[\#\}])'
t_MNUMERICAL = r'[ \t]*{[ \t]*\#[ \t]*(?=[=])'
t_LBRACKET   = r'{'
t_RBRACKET   = r'}'
t_CATEGORY   = r'^\$CATEGORY:.*$'

def t_newline(t):
    r'\n'
    t.lexer.lineno += 1
    t.lexer.linestart = t.lexer.lexpos

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    #t.lexer.skip(1)

lexer = lex.lex()

# To test lexer.
# lexer.input('You can use your pencil and paper for these next math questions.')
# while True:
#     tok = lexer.token()
#     if not tok: 
#         break      # No more input
#     print(tok)


# Yacc #######################################################################

def p_expression_gift(p):
    'gift : question_set'
    p[0] = p[1]


def p_expression_question_set(p):
    """
    question_set : question_set question
    question_set : question
    """
    if len(p) == 3 and isinstance(p[2], gift.Question):
        gift_result.add(p[2])
        p[0] = gift_result
    elif len(p) == 2 and isinstance(p[1], gift.Question):
        gift_result.add(p[1])
        p[0] = gift_result


def p_expresion_question(p):
    """
    question : CATEGORY
    question : QUESTION answer
    question : QUESTION missing QUESTIONC
    question : QUESTIOND
    """
    global category
    if len(p) == 2 and p[1].startswith('$CATEGORY:'):
        category = p[1][10:].strip()
        p[0] = category
    elif len(p) == 2:
        answer = gift.AnswerFactory.build(None)
        question = gift.QuestionFactory.build(
            p[1].strip(), answer, None, category
        )
        p[0] = question
    else:
        answer = p[2]
        text_continue = p[3][1:].strip() if len(p) == 4 else None
        question = gift.QuestionFactory.build(
            p[1].strip(), answer, text_continue, category
        )
        p[0] = question


def p_expression_missing(p):
    """
    missing : LBRACKET options
    missing : LBRACKET numerical
    """
    p[0] = gift.AnswerFactory.build(options=p[2])


def p_expression_answer(p):
    """
    answer : LBRACKET RBRACKET
    answer : LBRACKET options RBRACKET
    answer : LBRACKET truefalse RBRACKET
    answer : LBRACKET numerical RBRACKET
    answer : MNUMERICAL numerical RBRACKET
    """
    if len(p) == 3:
        p[0] = gift.AnswerFactory.build(options=[])
    elif len(p) == 4:
        p[0] = gift.AnswerFactory.build(options=p[2])


def p_expression_options(p):
    """
    options : options option
    options : option
    """
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = p[1] + [p[2]]


def p_expression_option(p):
    """
    option : OPTION FEEDBACK
    option : OPTION
    """
    if len(p) == 2:
        p[0] = gift.Option(text=p[1].strip())
    elif len(p) == 3:
        p[0] = gift.Option(text=p[1].strip(), feedback=p[2][1:].strip())


def p_expression_truefalse(p):
    """
    truefalse : TRUE FEEDBACK
    truefalse : FALSE FEEDBACK
    truefalse : TRUE
    truefalse : FALSE
    """
    text = 'True' if p[1].strip() in ['|TRUE', '|true', '|T', '|t'] else 'False'
    if len(p) == 3:
        p[0] = [ gift.Option(text=text, feedback=p[2][1:].strip()) ]
    elif len(p) == 2:
        p[0] = [ gift.Option(text=text) ]


def p_expression_numerical(p):
    """
    numerical : NUMERICAL FEEDBACK
    numerical : RANGE FEEDBACK
    numerical : NUMERICAL
    numerical : RANGE
    numerical : options
    """
    if len(p) == 3:
        p[0] = [ gift.Option(text=p[1].strip(), feedback=p[2][1:].strip()) ]
    elif len(p) == 2 and isinstance(p[1], str):
        p[0] = [ gift.Option(text=p[1].strip()) ]
    elif len(p) == 2 and isinstance(p[1], list):
        p[0] =  [ gift.Option(text='#' + opt.raw_text[1:], feedback=opt.feedback) for opt in p[1] ]


def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' in question number {len(gift_result.questions) + 1}. " + str(p))
        raise Exception(f"Syntax error at '{p.value}' in question number {len(gift_result.questions) + 1}.")
    else:
        print('Syntax error at EOI')
        raise Exception('Syntax error at EOI.')


parser = yacc.yacc()


def parse(s):
    res = preprocessor.preprocess(s)
    return parser.parse(res)
