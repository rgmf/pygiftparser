import re


def preprocess(s):
    # Removes comments and clean extra lines below and under the string.
    clean_s = ''
    for line in s.split('\n'):
        line = line.strip()
        if re.search(r'^::.*::.*$', line):
            line = re.sub(r'::', '}}', re.sub(r'::', '{{', line, 1), 1)

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
                res = res + '\n' + '\n'
        else:
            if num_newlines == 1:
                res = res + ' '
            num_newlines = 0
            c = ' ' if c == '\t' else c
            res = res + c

    return res.strip()