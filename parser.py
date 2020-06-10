from ply import lex
import ply.yacc as yacc


# Lex #########################################################################

# List of token names.
tokens = (
    'SLASH',
    'COLON',
    'OPEN_BRACE',
    'CLOSE_BRACE',
    'NEWLINE',
    'SCAPE',
    'CHAR'
)

# Regular expression rules for simple tokens.
t_COLON       = r':'
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
    gift_file : NEWLINE gift_file
    gift_file : question_name
    gift_file : question_name endquestion gift_file
    """
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[2]
    elif len(p) == 4:
        p[0] = p[1] + '\n' + p[3]

def p_expression_question_name(p):
    """
    question_name : COLON COLON string COLON COLON question
    question_name : COLON COLON string COLON COLON question OPEN_BRACE answer CLOSE_BRACE
    question_name : COLON COLON string COLON COLON question OPEN_BRACE NEWLINE answer NEWLINE CLOSE_BRACE
    """
    if len(p) == 7:
        p[0] = p[3] + ": " + p[6]
    elif len(p) == 10:
        p[0] = p[3] + ". " + p[6] + "(" + p[8] + ")"
    elif len(p) == 12:
        p[0] = p[3] + ". " + p[6] + "(" + p[9] + ")"


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

# Error rule for syntax errors
def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' in line {p.lineno}.")
        raise Exception(f"Syntax error at '{p.value}' in line {p.lineno}.")
    else:
        print('Syntax error at EOI')
        raise Exception('Syntax error at EOI: ' + p)

parser = yacc.yacc()
with open('file.gift', 'r') as myfile:
  s = myfile.read()
  #print('FICHERO')
  #print(s)
  #print()
  
  result = parser.parse(s)
  print('AQUÍ VA EL RESULTADO')
  print(result)
