import argparse


def getArguments():
    parser = argparse.ArgumentParser(description='Debatable Application')
    parser.add_argument('--link', type=str, help='A link to a web page')
    parser.add_argument('--path',
                        type=str,
                        help='A path to .txt file with a list of web pages')

    return parser.parse_args()