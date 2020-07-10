# Python Moodle GIFT parser
Python Moodle GIFT parser is a parser for GIFT files: https://docs.moodle.org/38/en/GIFT_format

The program consist in two parts: `parser.py` with lex/yacc and `gift.py` with classes where parser results will saved. The class `Gift` will contain all questions and every `Question` will have an answer (there are several types of answers - read the Moodle GIFT documentation).

# How to run (use) the parser
There is an `example.py` script python with an example. This script expect a file and parse it. After that it prints the object `Gift` with all information catched by the parser.

# Use it like a package in your own project
You can install it like a package using `pip` from pypi.org: `pip install pygiftparserrgmf`.

After that, you can parse a file like this:

```python
from pygiftparserrgmf import parser

with open('gift_file.txt', 'r') as myfile:
    s = myfile.read()
    gift_object = parser.parse(s)
```

From here you'll have `Gift` object into `gift_object` (see `pygiftparser/gift.py` file).

# Hot to test the parser
Inside `tests` folder there are several tests. You can run all of them executing the command `python -m unittest discover -v -s tests/`.
