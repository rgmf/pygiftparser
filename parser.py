import argparse
import re
from ply import lex
import ply.yacc as yacc

import answers
import preprocessor


# Lex #########################################################################

# List of token names.
tokens = (
    'SLASH',
    'COLONCOLON',
    'OPEN_BRACE',
    'CLOSE_BRACE',
    'NEWLINE',
    'SCAPE',
    'CORRECT',
    'WRONG',
    'CHAR'
)

# Regular expression rules for simple tokens.
t_COLONCOLON  = r'::'
t_OPEN_BRACE  = r'{'
t_CLOSE_BRACE = r'}'
t_SCAPE       = r'\\.'
t_CHAR        = r'[^\{\}\n]' # everything less the other tokens.
def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    return t

#t_ignore = ' \t'

# Ignore comments.
def t_COMMENT(t):
    r'^[ \t]*//.*'
    pass

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
    'goal : n_nl gift'
    p[0] = p[2]


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
    question_type : COLONCOLON string COLONCOLON question
    question_type : question
    """
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 5:
        p[0] = p[2] + ': ' + p[4]


def p_expression_question(p):
    'question : string brace_expr'
    p[0] = p[1] + p[2]


def p_expression_brace_expr(p):
    """
    brace_expr :
    brace_expr : OPEN_BRACE CLOSE_BRACE
    brace_expr : OPEN_BRACE answer CLOSE_BRACE
    """
    if len(p) == 1:
        p[0] = ''
    elif len(p) == 3:
        p[0] = ''
    elif len(p) == 4:
        p[0] = p[2]


def p_expression_answer(p):
    """
    answer : string
    """
    clean_string = p[1].strip()

    # Is it a multiple answer?
    pattern = re.compile(r'^[=~]{1}|[^\\][=~]{1}')
    n = len(re.findall(pattern, clean_string))
    if n > 1:
        res = ''
        pos = 0
        copy_string = clean_string
        for i in range(n):
            a = answers.get_first_answer(copy_string)
            clean_a = a.strip()
            res = res + str(answers.create_answer(clean_a))
            pos = len(a)
            copy_string = copy_string[pos:]
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


def p_expression_n_nl(p):
    """
    n_nl :
    n_nl : n_nl NEWLINE
    """


# Error rule for syntax errors
def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' in line {p.lineno}.")
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
  result = parser.parse(res)
  print('AQUÍ VA EL RESULTADO')
  print(result)
