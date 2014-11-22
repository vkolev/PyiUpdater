import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli_ui.ui.menu_utils import (get_correct_answer, path_fixer,
                               _directory_fixer)


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


def test_path_fixer():
    path = u'/Home Folder/Next Folder/Someone/Not Me/Test'
    fixed_path = u'/Home\ Folder/Next\ Folder/Someone/Not\ Me/Test'
    assert fixed_path == path_fixer(path)


def test_directory_fixer():
    assert u'/home/jms' == _directory_fixer(u'/home/jms')


def test_directory_fixer_home_shortcut():
    assert os.path.join(os.path.expanduser(u'~'),
                        u'Downloads') == _directory_fixer(u'~/Downloads')


def test_directory_fixer_home_direcotry_symbol():
    downlaods_dir = os.path.join(os.path.expanduser(u'~'), u'Downloads')
    assert downlaods_dir == _directory_fixer(u'~/Downloads')
