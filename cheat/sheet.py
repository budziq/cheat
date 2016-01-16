from cheat import sheets 
from cheat import utils
from cheat.utils import *
import os
import shutil
import subprocess


def copy(current_sheet_path, new_sheet_path):
    """ Copies a sheet to a new path """

    # attempt to copy the sheet to DEFAULT_CHEAT_DIR
    try:
        shutil.copy(current_sheet_path, new_sheet_path)

    # fail gracefully if the cheatsheet cannot be copied. This can happen if
    # DEFAULT_CHEAT_DIR does not exist
    except IOError:
        die ('Could not copy cheatsheet for editing.')


def create_or_edit(sheet):
    """ Creates or edits a cheatsheet """

    # if the cheatsheet does not exist
    if not exists(sheet):
        create(sheet)

    # if the cheatsheet exists but not in the default_path, copy it to the
    # default path before editing
    elif exists(sheet) and not exists_in_default_path(sheet):
        copy(path(sheet), os.path.join(sheets.default_path(), sheet))
        edit(sheet)

    # if it exists and is in the default path, then just open it
    else:
        edit(sheet)


def create(sheet):
    """ Creates a cheatsheet """
    new_sheet_path = os.path.join(sheets.default_path(), sheet)

    try:
        subprocess.call([editor(), new_sheet_path])

    except OSError:
        die('Could not launch ' + editor())


def edit(sheet):
    """ Opens a cheatsheet for editing """

    try:
        subprocess.call([editor(), path(sheet)])

    except OSError:
        die('Could not launch ' + editor())


def exists(sheet):
    """ Predicate that returns true if the sheet exists """
    return sheet in sheets.get() and os.access(path(sheet), os.R_OK)


def exists_in_default_path(sheet):
    """ Predicate that returns true if the sheet exists in default_path"""
    default_path_sheet = os.path.join(sheets.default_path(), sheet)
    return sheet in sheets.get() and os.access(default_path_sheet, os.R_OK)


def is_writable(sheet):
    """ Predicate that returns true if the sheet is writeable """
    return sheet in sheets.get() and os.access(path(sheet), os.W_OK)


def path(sheet):
    """ Returns a sheet's filesystem path """
    return sheets.get()[sheet]


def read(sheet):
    """ Returns the contents of the cheatsheet as a String """
    if not exists(sheet):
        die('No cheatsheet found for ' + sheet)

    with open (path(sheet)) as cheatfile:
          return cheatfile.read()


def enumerate_entries(sheet, range_text):
    """ Returns the contents of the cheatsheet as a String with entries
    preceded by line numbers. If line number range is given return only
    the entries requested lines without comment and blank lines. """

    if not exists(sheet):
        die('No cheatsheet found for ' + sheet)

    with open(path(sheet)) as cheatfile:
        lines = enumerate_if(is_command, cheatfile.readlines())
        line_range = parse_range(range_text)
        if line_range:
            # print just uncolored raw lines in given ranges
            lines = [line for num, line in lines if num in line_range]
        else:
            # print colored lines prepended with line numbers
            lines = [colorize(number_line(num, line)) for num, line in lines]
        return ''.join(lines)
