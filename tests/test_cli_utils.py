import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyi_updater.utils import (get_correct_answer,
                               directory_fixer)


def test_get_correct_answer():
    correct_answer = u'Yea Boy'
    result = get_correct_answer(u'Fav. phrase', answer=correct_answer,
                                is_answer_correct=u'yes')

    assert result == correct_answer


def test_get_correct_answer_default():
    correct_answer = 'Yea Boy'
    result = get_correct_answer(u'Fav. phrase', answer=u'',
                                default=correct_answer,
                                is_answer_correct=u'yes')
    assert result == correct_answer


def test_directory_fixer():
    assert u'/home/jms' == directory_fixer(u'/home/jms')


def test_directory_fixer_home_shortcut():
    assert os.path.join(os.path.expanduser(u'~'),
                        u'Downloads') == directory_fixer(u'~/Downloads')


def test_directory_fixer_home_direcotry_symbol():
    downlaods_dir = os.path.join(os.path.expanduser(u'~'), u'Downloads')
    assert downlaods_dir == directory_fixer(u'~/Downloads')
