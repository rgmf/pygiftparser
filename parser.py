import argparse
import re
from ply import lex
import ply.yacc as yacc

import answers
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
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 5:
        p[0] = p[1] + '\n' + p[4]


def p_expression_question_type(p):
    """
    question_type : OPEN_BRACE OPEN_BRACE string CLOSE_BRACE CLOSE_BRACE question
    question_type : question
    """
    if len(p) == 2:
        p[0] = p[1]
        question = gift_result.questions[-1]
        question.name = question.text
    elif len(p) == 7:
        p[0] = p[3].strip() + ': ' + p[6]
        question = gift_result.questions[-1]
        question.name = p[3].strip()


def p_expression_question(p):
    'question : string brace_expr'
    p[0] = p[1].strip() + p[2]

    question = gift.Question()
    question.text = p[1].strip()
    gift_result.add(question)


def p_expression_brace_expr(p):
    """
    brace_expr :
    brace_expr : OPEN_BRACE CLOSE_BRACE
    brace_expr : OPEN_BRACE answer CLOSE_BRACE question_continue
    """
    if len(p) == 1:
        p[0] = ''
    elif len(p) == 3:
        p[0] = ''
    elif len(p) == 5:
        p[0] = p[2] + p[4]


def p_expression_question_continue(p):
    """
    question_continue :
    question_continue : string
    """
    if len(p) == 1:
        p[0] = ''
    elif len(p) == 2:
        p[0] = ' MISSING_WORD_CONTINUE(' + p[1].strip() + ')'


def p_expression_answer(p):
    'answer : string'
    clean_string = p[1].strip()

    # Is it a multiple answer?
    pattern = re.compile(r'^[=~]{1}|[^\\][=~]{1}')
    n = len(re.findall(pattern, clean_string))
    if n > 1:
        res = ''
        pos = 0
        for i in range(n):
            answer = answers.get_first_answer(clean_string)
            clean_answer = answer.strip()
            res = res + str(answers.create_answer(clean_answer))
            pos = len(answer)
            clean_string = clean_string[pos:]
    else:
        res = answers.create_answer(p[1].strip())

    p[0] = '(' + str(res) + ')'


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


##############################################################################

def parse_input_arguments():
    parser = argparse.ArgumentParser(description='GIFT Moodle file parser.')
    parser.add_argument('-f', '--file', dest='file', required=True,
                        help='GIFT Moodle file.')
    args = parser.parse_args()
    return args


args = parse_input_arguments()
with open(args.file, 'r') as myfile:
    s = myfile.read()
    #print('FICHERO')
    #print(s)
    #print()
  
    res = preprocessor.preprocess(s)
    print('RESULTADO DEL PREPROCESADOR')
    print(res)
    print()
    result = parser.parse(res)
    print('AQUÍ VA EL RESULTADO DEL PARSER')
    print(result)


    print()
    print()
    print('AQUÍ EL OBJETO')
    for q in gift_result.questions:
        print(q.name + ': ' + q.text)
