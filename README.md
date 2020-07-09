# Status
This program has been tested with all GIFT files that you can find inside `example_files`. Also, it has been developed unit tests and all of them passed.

Nevertheless it's in an alpha status because it needs more robust tests and this must not be used in production.

Use it in your own risk.

# Python Moodle GIFT parser
Python Moodle GIFT parser is a parser for GIFT files: https://docs.moodle.org/38/en/GIFT_format

The program consist in two parts: `parser.py` with lex/yacc and `gift.py` with classes where parser results will saved. The class `Gift` will contain all questions and every `Question` will have an answer (there are several types of answers - read the Moodle GIFT documentation).

# How to run (use) the parser
There is an `example.py` script python with an example. This script expect a file and parse it. After that it prints the object `Gift` with all information catched by the parser.

# Hot to test the parser
Inside `tests` folder there are several tests. You can run all of them executing the command `python -m unittest -v discover -s tests/`.
