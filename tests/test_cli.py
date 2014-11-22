import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_cli_import():
    try:
        import cli_ui
        import_test = True
    except ImportError:
        import_test = False

    assert import_test is True
