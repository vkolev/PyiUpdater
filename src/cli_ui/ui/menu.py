from __future__ import print_function
import logging
import os
import sys

from jms_utils.terminal import get_terminal_size, GetCh
from six.moves import xrange

from pyi_updater.version import get_version

if sys.platform == u'win32':
    clear = u'cls'
else:
    clear = u'clear'


log = logging.getLogger(__name__)


class Menu(object):

    def __init__(self, name=None, options=None, message=None):
        self.menu_name = name
        self.message = message
        self.options = options

    def __call__(self):
        x = self.display()
        if len(x) == 2:
            next_ = x[1]
            next_()
        # We are dynamically generating upload options
        # from installed plugins. So the option selected
        # by the user needs a little extra processing
        else:
            name = x[0]
            func = x[1]
            func(name)

    def display(self):
        self.display_menu_header(self.menu_name)
        self.display_msg(self.message)
        return self.menu_options(self.options)

    # Takes a string and adds it to the menu header along side
    # the app name.
    def display_menu_header(self, page_name=None):

        window_size = get_terminal_size()[0]

        def add_style():
            app = u'PyiUpdater v{}'.format(get_version())
            top = u'*' * window_size + u'\n'
            bottom = u'\n' + u'*' * window_size + u'\n'
            if page_name is not None:
                header = app + u' - ' + page_name
            else:
                header = app

            header = header.center(window_size)
            msg = top + header + bottom
            return msg
        os.system(clear)
        print(add_style())

    def display_msg(self, message=None):
        window_size = get_terminal_size()[0]
        if message is None:
            return u''

        if not isinstance(message, str):
            log.warning(u'Did not pass str')
            return u''

        def format_msg():
            formatted = []
            finished = [u'\n']
            count = 0
            words = message.split(' ')
            for w in words:
                w = w + u' '
                if count + len(w) > window_size / 2:
                    finished.append(''.join(formatted).center(window_size))
                    finished.append('\n')
                    count = len(w)
                    # Starting a new line.
                    formatted = []
                    formatted.append(w)
                else:
                    formatted.append(w)
                    count += len(w)
            finished.append(u''.join(formatted).center(window_size))
            finished.append(u'\n')
            return u''.join(finished)
        print(format_msg())

    # Takes a list of tuples(menu_name, call_back) adds menu numbers
    # then prints menu to screen.
    # Gets input from user, then returns the callback
    def menu_options(self, options=None):
        if options is None:
            return u""
        if not isinstance(options, list):
            log.error(u'Must pass "list" not "{}"'.format(type(options)))
            return u""
        log.debug(u'Passed in options: {}'.format(options))

        def add_options():
            getch = GetCh()
            menu = []
            count = 1
            for s in options:
                item = u'{}. {}\n'.format(count, s[0])
                menu.append(item)
                if count == 9:
                    # Using getch() to capture a single character
                    # then reutrn. For example trying to input 10
                    # would only capture the 1 then return
                    break
                count += 1
            print(u''.join(menu))
            answers = []
            for a in xrange(1, len(menu) + 1):
                answers.append(str(a))
            while 1:
                ans = getch()
                if ans in answers:
                    break
                else:
                    log.debug(u'Not an acceptable answer!')
            return options[int(ans) - 1]
        return add_options()
