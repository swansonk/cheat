from __future__ import print_function
import os
import subprocess
import sys

def highlight(needle, haystack):
    """ Highlights a search term matched within a line """

    # if colorization is not configured, exit early
    if os.environ.get('CHEATCOLORS') != 'true':
        return sheet_content

    # otherwise, attempt to import the termcolor library
    try:
        from termcolor import colored

    # if the import fails, return uncolored text
    except ImportError:
        return haystack

    # if the import succeeds, colorize the needle in haystack
    return haystack.replace(needle, colored(needle, 'blue'));

def colorize(sheet_content):
    """ Colorizes cheatsheet content if so configured """

    # if colorization is not configured, exit early
    if os.environ.get('CHEATCOLORS') != 'true':
        return sheet_content

    # otherwise, attempt to import the pygments library
    try:
        from pygments import highlight
        from pygments.lexers import get_lexer_by_name
        from pygments.formatters import TerminalFormatter

    # if the import fails, return uncolored text
    except ImportError:
        return sheet_content

    # otherwise, attempt to colorize
    first_line = sheet_content.splitlines()[0]
    lexer      = get_lexer_by_name('bash')
    if first_line.startswith('```'):
        sheet_content = '\n'.join(sheet_content.split('\n')[1:-2])
        try:
            lexer = get_lexer_by_name(first_line[3:])
        except Exception:
            pass

    return highlight(sheet_content, lexer, TerminalFormatter())


def die(message):
    """ Prints a message to stderr and then terminates """
    warn(message)
    exit(1)


def editor():
    """ Determines the user's preferred editor """

    # determine which editor to use
    editor = os.environ.get('CHEAT_EDITOR') \
        or os.environ.get('VISUAL')         \
        or os.environ.get('EDITOR')         \
        or False

    # assert that the editor is set
    if editor == False:
        die(
            'You must set a CHEAT_EDITOR, VISUAL, or EDITOR environment '
            'variable in order to create/edit a cheatsheet.'
        )

    return editor


def open_with_editor(filepath):
    """ Open `filepath` using the EDITOR specified by the environment variables """
    editor_cmd = editor().split()
    try:
        subprocess.call(editor_cmd + [filepath])
    except OSError:
        die('Could not launch ' + editor())


def warn(message):
    """ Prints a message to stderr """
    print((message), file=sys.stderr)
