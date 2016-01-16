from __future__ import print_function
import os
import sys


def colorize(sheet_content):
    """ Colorizes cheatsheet content if so configured """

    # only colorize if so configured
    if not 'CHEATCOLORS' in os.environ:
        return sheet_content

    try:
        from pygments import highlight
        from pygments.lexers import BashLexer
        from pygments.formatters import TerminalFormatter

    # if pygments can't load, just return the uncolorized text
    except ImportError:
        return sheet_content

    return highlight(sheet_content, BashLexer(), TerminalFormatter())


def die(message):
    """ Prints a message to stderr and then terminates """
    warn(message)
    exit(1)


def editor():
    """ Determines the user's preferred editor """
    if 'EDITOR' not in os.environ:
        die(
            'In order to create/edit a cheatsheet you must set your EDITOR '
            'environment variable to your editor\'s path.'
        )

    elif os.environ['EDITOR'] == "":
        die(
          'Your EDITOR environment variable is set to an empty string. It must '
          'be set to your editor\'s path.'
        )

    else:
        return os.environ['EDITOR']


def prompt_yes_or_no(question):
    """ Prompts the user with a yes-or-no question """
    # Support Python 2 and 3 input
    # Default to Python 2's input()
    get_input = raw_input
 
    # If this is Python 3, use input()
    if sys.version_info[:2] >= (3, 0):
        get_input = input

    print(question)
    return get_input('[y/n] ') == 'y'


def warn(message):
    """ Prints a message to stderr """
    print((message), file=sys.stderr)


def is_command(line):
    """test if text line has any text that is not comment and whitespace"""
    line = line.strip()
    return line and not line.startswith('#')


def enumerate_if(cond, sequence, start=0):
    """conditional version of std library enumerate"""
    count = start
    for elem in sequence:
        if cond(elem):
            yield count, elem
            count += 1
        else:
            yield None, elem


def number_line(num, line):
    """reformat line if there is additional sequence number"""
    if num is not None:
        return '({NUM}) {LINE}'.format(NUM=num, LINE=line)
    return line


def parse_range(text):
    """parse text in page printer like algorithm to generate int ranges"""
    res = set()
    if not text:
        return res

    for item in text.split(','):
        beg, _, end = item.partition('-')
        if beg.isdigit():
            if end.isdigit():
                res = res.union(range(int(beg), int(end)+1))
            else:
                res.add(int(beg))
    return res
