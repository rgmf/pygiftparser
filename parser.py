import argparse
from ply import lex
import ply.yacc as yacc


# Lex #########################################################################

# List of token names.
tokens = (
    'SLASH',
    'COLONCOLON',
    'OPEN_BRACE',
    'CLOSE_BRACE',
    'NEWLINE',
    'SCAPE',
    'CHAR'
)

# Regular expression rules for simple tokens.
t_COLONCOLON       = r'::'
t_OPEN_BRACE  = r'{'
t_CLOSE_BRACE = r'}'
t_SCAPE       = r'\\.'
t_CHAR        = r'[^:\{\}\n\\]' # everything less the other tokens.
def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    return t

# t_ignore = ' \t'

# Ignore comments.
def t_COMMENT(t):
    r'[ \t]*//.*'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.lexer.linestart = t.lexer.lexpos

# Error.
def t_error(t):
    print('Illegal character "%s"' % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()


# Yacc ########################################################################

def p_expression_gift_file(p):
    """
    gift_file : optional_newline
    gift_file : NEWLINE gift_file
    gift_file : question_expr
    gift_file : question_expr endquestion gift_file
    """
    if len(p) == 2 and p[1] != 'NEWLINE':
        p[0] = ''
    elif len(p) == 2 and p[1] == 'NEWLINE':
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[2]
    elif len(p) == 4 and p[3] != '':
        p[0] = p[1] + '\n' + p[3]
    elif len(p) == 4 and p[3] == '':
        p[0] = p[1]


def p_expression_question_expr(p):
    """
    question_expr : question_noname_expr
    question_expr : question_withname_expr
    """
    p[0] = p[1]


def p_expression_question_withname_expr(p):
    """
    question_withname_expr : COLONCOLON string COLONCOLON question
    question_withname_expr : COLONCOLON string COLONCOLON question OPEN_BRACE optional_newline CLOSE_BRACE
    question_withname_expr : COLONCOLON string COLONCOLON question OPEN_BRACE optional_newline answer optional_newline CLOSE_BRACE
    """
    if len(p) == 5 or len(p) == 8:
        p[0] = p[2] + ": " + p[4]
    elif len(p) == 10:
        p[0] = p[2] + ": " + p[4] + "(" + p[7] + ")"


def p_expression_question_noname_expr(p):
    """
    question_noname_expr : question
    question_noname_expr : question OPEN_BRACE optional_newline CLOSE_BRACE
    question_noname_expr : question OPEN_BRACE optional_newline answer optional_newline CLOSE_BRACE
    """
    if len(p) == 2 or len(p) == 5:
        p[0] = p[1]
    elif len(p) == 7:
        p[0] = p[1] + "(" + p[4] + ")"


def p_expression_string(p):
    """
    string : CHAR
    string : CHAR string
    """
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1] + p[2]


def p_expression_question(p):
    """
    question : string
    """
    p[0] = p[1]


def p_expression_answer(p):
    """
    answer : string
    answer : answer NEWLINE string
    """
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[1] + ", " + p[3]


def p_expression_endquestion(p):
    'endquestion : NEWLINE NEWLINE'


def p_expression_optional_newline(p):
    """
    optional_newline :
    optional_newline : NEWLINE optional_newline
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
    parser = argparse.ArgumentParser(description='Stats generator about subjects sessions.')
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
  
  result = parser.parse(s)
  print('AQUÍ VA EL RESULTADO')
  print(result)
