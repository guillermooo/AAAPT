import sublime
import sublime_plugin

from itertools import chain
import io
import os
import unittest
import tempfile


# A tuple: (low level file_descriptor, path) as returned by `tempfile.mkstemp()`.
TEST_DATA_PATH = None


def make_temp_file():
    global TEST_DATA_PATH
    TEST_DATA_PATH = tempfile.mkstemp()


class TestsState(object):
    running = False
    view = None
    suite = None

    @staticmethod
    def reset():
        TestsState.suite = None

    @staticmethod
    def reset_window_settings(names):
        for name in names:
            TestsState.view.window().settings().erase(name)

    @staticmethod
    def reset_view_settings(names):
        for name in names:
            TestsState.view.settings().erase(name)


def combine(suite):
    # Combine all tests under one key for convenience. Ignore keys starting with an underscore. Use
    # these for subsets of all the remaining tests that you don't want repeated under '_all_'.
    # Convert to list so the 'chain' doesn't get exhausted after the first use.
    all_tests = list(chain(*(data for (key, data)
                                  in suite.items()
                                  if not key.startswith('_'))))
    suite['_all_'] = all_tests
    return suite


def register_tests(suite):
    _xpt_show_suites.suite = combine(suite)


class _xpt_show_suites(sublime_plugin.WindowCommand):
    '''Displays a quick panel listing all available test stuites.
    '''
    suite = None

    @staticmethod
    def register(suite):
        _xpt_show_suites.suite = combine(suite)

    def run(self):
        TestsState.running = True
        self.window.show_quick_panel(sorted(_xpt_show_suites.suite.keys()), self.on_done)

    def on_done(self, idx):
        if idx == -1:
            sublime.status_message('_PackageTesting: No test suite selected.')
            return

        suite_name = sorted(_xpt_show_suites.suite.keys())[idx]
        TestsState.suite = suite_name

        self.window.run_command('_xpt_run_tests')


class _xptPrintResults(sublime_plugin.TextCommand):
    def run(self, edit, content):
        view = sublime.active_window().new_file()
        view.insert(edit, 0, content)
        view.set_scratch(True)


class _xptRunTests(sublime_plugin.WindowCommand):
    def run(self):
        make_temp_file()
        # We open the file here, but Sublime Text loads it asynchronously, so we continue in an
        # event handler, once it's been fully loaded.
        self.window.open_file(TEST_DATA_PATH[1])


class _xptTestDataDispatcher(sublime_plugin.EventListener):
    def on_load(self, view):
        if TEST_DATA_PATH:
            try:
                if (view.file_name() and view.file_name() == TEST_DATA_PATH[1] and
                    TestsState.running):

                        TestsState.running = False
                        TestsState.view = view

                        suite_names = _xpt_show_suites.suite[TestsState.suite]
                        suite = unittest.TestLoader().loadTestsFromNames(suite_names)

                        bucket = io.StringIO()
                        unittest.TextTestRunner(stream=bucket, verbosity=1).run(suite)

                        view.run_command('_xpt_print_results', {'content': bucket.getvalue()})
                        w = sublime.active_window()
                        # Close data view.
                        w.run_command('prev_view')
                        TestsState.view.set_scratch(True)
                        w.run_command('close')
                        w.run_command('next_view')
                        # Ugly hack to return focus to the results view.
                        w.run_command('show_panel', {'panel': 'console', 'toggle': True})
                        w.run_command('show_panel', {'panel': 'console', 'toggle': True})
            except Exception as e:
                print(e)
            finally:
                try:
                    os.close(TEST_DATA_PATH[0])
                except Exception as e:
                    print('Could not close temp file...')
                    print(e)


class WriteToBuffer(sublime_plugin.TextCommand):
    '''Replaces the buffer's content with the specified `text`.

       `text`: Text to be written to the buffer.
       `file_name`: If this file name does not match the receiving view's, abort.
    '''
    def run(self, edit, file_name='', text=''):
        if not file_name:
            return

        if self.view.file_name().lower() == file_name.lower():
            self.view.replace(edit, sublime.Region(0, self.view.size()), text)
