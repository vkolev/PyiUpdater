from __future__ import print_function
import logging
import os
import sys


from six.moves import input

log = logging.getLogger(__name__)


def ask_yes_no(question, default='no', answer=None):
    """Will ask a question and keeps prompting until
    answered.

    Args:
        question (str): Question to ask end user

    Kwargs:
        default (str): Default answer if user just press enter at prompt

    Returns:
        bool. Meaning::

            True - Answer is  yes

            False - Answer is no
    """
    default = default.lower()
    yes = [u'yes', u'ye', u'y']
    no = [u'no', u'n']
    if default in no:
        help_ = u'[N/y]?'
        default = False
    else:
        default = True
        help_ = u'[Y/n]?'
    while 1:
        display = question + '\n' + help_
        if answer is None:
            log.debug(u'Under None')
            answer = input(display)
            answer = answer.lower()
        if answer == u'':
            log.debug(u'Under blank')
            return default
        if answer in yes:
            log.debug(u'Must be true')
            return True
        elif answer in no:
            log.debug(u'Must be false')
            return False
        else:
            sys.stdout.write(u'Please answer yes or no only!\n\n')
            sys.stdout.flush()
            answer = None
            input(u'Press enter to continue')
            sys.stdout.write('\n\n\n\n\n')
            sys.stdout.flush()


def get_correct_answer(question, default=None, required=False,
                       answer=None, is_answer_correct=None):
    while 1:
        if default is None:
            msg = u' - No Default Available'
        else:
            msg = (u'\n[DEFAULT] -> {}\nPress Enter To '
                   'Use Default'.format(default))
        prompt = question + msg + '\n--> '
        if answer is None:
            answer = input(prompt)
        if answer == '' and required and default is not None:
            print(u'You have to enter a value\n\n')
            input(u'Press enter to continue')
            print('\n\n')
            answer = None
            continue
        if answer == u'' and default is not None:
            answer = default
        _ans = ask_yes_no(u'You entered {}, is this '
                          'correct?'.format(answer),
                          answer=is_answer_correct)
        if _ans:
            return answer
        else:
            answer = None


# Makes inputting directory more like shell
def _directory_fixer(_dir):
    if _dir.startswith(u'~'):
        log.debug(u'Expanding ~ to full user path')
        _dir = _dir[2:]
        _dir = os.path.join(os.path.expanduser(u'~'), _dir)
    return _dir


# Fixed path to work without quotes
def path_fixer(path):
    # Removing ' & " in case user used them
    # for path with spaces
    path.replace(u"'", u"")
    path.replace(u'"', u'')

    # Escaping spaces in path
    return path.replace(' ', '\ ')
