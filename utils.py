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
        TestsState.reset_window_settings('vintage')
        TestsState.reset_view_settings('vintage')

        self.view = TestsState.view
        self.view.sel().clear()

    def R(self, a, b):
        return R(self.view, a, b)

    def set_text(self, text):
        set_text(self.view, text)

    def add_sel(self, a, b):
        add_sel(self.view, a, b)

    def get_sel(self, num):
        return get_sel(self.view, num)

    def first_sel(self):
        return first_sel(self.view)

    def second_sel(self):
        return second_sel(self.view)

    def last_sel(self):
        return last_sel(self.view)


def R(view, a, b):
    """
    Creates a new region. Can be used in two ways:

        1. To make a region from point a to point b:

            r = R(10, 15)

        2. To make a region spanning specific lines:

            # Tuples specify (row, col) as returned by view.rowcol().
            r = R((0, 10), (3, 15))
    """
    try:
        pt_a = view.text_point(*a)
        pt_b = view.text_point(*b)
        return sublime.Region(pt_a, pt_b)
    except (TypeError, ValueError):
        pass

    if (isinstance(a, int) and isinstance(b, int)):
        return sublime.Region(a, b)
    raise ValueError("a and b parameters must be either ints or (int, int)")


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
