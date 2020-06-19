import re


def preprocess(s):
    # Removes comments and clean extra lines below and under the string.
    clean_s = ''
    for line in s.split('\n'):
        line = line.strip()
        if not re.search(r'^//.*$', line):
            clean_s = clean_s + line + '\n'
    clean_s = clean_s.strip()

    # All questions in a line and a blank line between questions.
    res = ''
    num_newlines = 0
    for c in clean_s:
        if c == '\n':
            num_newlines = num_newlines + 1
            if num_newlines == 2:
                res = res + '\n'
        else:
            if num_newlines == 1:
                res = res + ' '
            num_newlines = 0
            c = ' ' if c == '\t' else c
            res = res + c

    # Convert true-false answers to =TRUE or =FALSE.
    true_p = r'{[ \t]*TRUE[ \t]*?(?=[\}\#])|{[ \t]*true[ \t]*?(?=[\}\#])|{[ \t]*T[ \t]*?(?=[\}\#])|{[ \t]*t[ \t]*?(?=[\}\#])'
    false_p = r'{[ \t]*FALSE[ \t]*?(?=[\}\#])|{[ \t]*false[ \t]*?(?=[\}\#])|{[ \t]*F[ \t]*?(?=[\}\#])|{[ \t]*f[ \t]*?(?=[\}\#])'
    res = re.sub(true_p, '{|TRUE', res)
    res = re.sub(false_p, '{|FALSE', res)

    return res.strip()