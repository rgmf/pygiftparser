This software is activily current testing and it's not ready for use it.

# Python Moodle GIFT parser
Python Moodle GIFT parser is a parser for GIFT files: https://docs.moodle.org/38/en/GIFT_format

The program consist in two parts: `parser.py` with lex/yacc and `gift.py` with classes where parser results will saved. The class `Gift` will contain all questions and every `Question` will have an answer (there are several types of answers - read the Moodle GIFT documentation).

# How to run (use) the parser
There is a `test.py` with an example. This script expect a file and parse it. After that it prints the object `Gift` with all information catched by the parser.