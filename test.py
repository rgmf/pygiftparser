import parser
import argparse


def parse_input_arguments():
    parser = argparse.ArgumentParser(description='GIFT Moodle file parser.')
    parser.add_argument('-f', '--file', dest='file', required=True,
                        help='GIFT Moodle file.')
    args = parser.parse_args()
    return args


args = parse_input_arguments()
with open(args.file, 'r') as myfile:
    s = myfile.read()
    result = parser.parse(s)
    for q in result.questions:
        print('QUESTION: ' + q.name)
        print('TYPE: ' + q.answer.__repr__())
        print(q.text)
        print(q.answer)
        print()
