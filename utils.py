import sublime
import unittest

from AAAPT.runner import TestsState


class BufferTest(unittest.TestCase):
    """
    TestCases can subclass from this base class to be able to run tests against
    a view more easily. If you use BufferTest, you don't have to manually
    import TestsState for basic uses.
    """
    def setUp(self):
        TestsState.reset()
        TestsState.reset_window_settings('vintage')
        TestsState.reset_view_settings('vintage')

        self.view = TestsState.view
        self.view.sel().clear()

    def R(self, a, b):
        return make_region(self.view, a, b)


def make_region(view, a, b):
    """
    Creates a new selection. Can be used in two ways:

        make_region(10, 15) => Makes a region spanning from 10 to 15.
        make_region((0, 10), (3, 15)) => Makes a region spanning from 10th col
                                         in row 0 to 15th col in row 3.
    """
    try:
        pt_a = view.text_point(*a)
        pt_b = view.text_point(*b)
        return sublime.Region(pt_a, pt_b)
    except (TypeError, ValueError):
        pass

    if (isinstance(a, int) and isinstance(b, int)):
        return sublime.Region(a, b)
    raise ValueError("a and b parameters must be either ints or (row, col)")


def set_text(view, text):
    # TODO: use 'append' instead (built-in).
    view.run_command('write_to_buffer', {'text': text,
                                         'file_name': view.file_name()})


def add_sel(view, a=0, b=0):
    if isinstance(a, sublime.Region):
        view.sel().add(a)
        return
    view.sel().add(sublime.Region(a, b))


def get_sel(view, num):
    return view.sel()[num]


def count_sels(view):
    return len(view.sel())


def first_sel(view):
    return get_sel(view, 0)


def second_sel(view):
    return get_sel(view, 1)


def last_sel(view):
    return get_sel(view, -1)
