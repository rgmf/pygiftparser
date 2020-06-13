def preprocess(s):
    s = s.strip()
    res = ''
    num_newlines = 0
    for c in s:
        if c == '\n':
            num_newlines = num_newlines + 1
            if num_newlines == 2:
                res = res + '\n' + '\n'
        else:
            num_newlines = 0
            c = ' ' if c == '\t' else c
            res = res + c

    print('PREPROCESSADOR')
    print(res.strip())
    print()
    return res.strip()