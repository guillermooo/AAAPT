AAAPT
=====

Package Tests - a test framework for Sublime Text packages.


Installation
------------

1. Download the [latest build](https://bitbucket.org/guillermooo/aaapt/downloads/AAAPT.sublime-package)
2. Copy *AAAPT.sublime-package* to *Packages/Installed Packages*
3. Restart Sublime Text.

To locate *Packages/Installed Packages*, you can open the console (<kbd>Ctrl</kbd>+<kbd>`</kbd>) and run this:

```python
sublime.installed_packages_path()
```


How to Use
----------

AAAPT lets you run tests in the context of Sublime Text. To use AAAPT correctly you need to ensure
two things:

* Your package has specified tests to be run by AAAPT
* There's no other currently loaded *.sublime-package* that includes AAPT tests

Specifying tests is easy. Simply create a file like *test_harness.py* at the top level of your
*FooPackage.sublime-package* and include something like this:

```python
from AAAPT.runner import register_tests

test_suites = {
	'baz': ['FooPackage.tests.test_baz'],
}

register_tests(test_suites)
``` 

Now you can write the still inexistent tests. First we create a file to hold them:

```bash
cd path/to/FooPackage
touch tests/test_baz.py
```

Then we write the tests:

```python
import unittest

from AAAPT.utils import BufferTest


# Test that uses AAAPT's helpers.
class Test_BufferSample(BufferTest):
    def testSample(self):
    	self.set_text('foo bar\nfizz buzz\n')
    	self.add_sel(self.R((1, 0), (1, 4)))	
        self.assertEqual(self.view.substr(self.first_sel()), 'fuzz')


# Regular test.
class Test_Sample(unittest.TestCase):
    def testSample(self):
        self.assertTrue(False)
```

Finally, we can publish *FooPackage.sublime-package* to *Packages/Installed Packages*, restart
Sublime Text and, from the Command Palette, select **Run Active Tests...**. The results of the
test run will be printed to a new view.


Donate
------

If you like this package and want to thank me, you can do so here:

Paypal
Gittip
Pledgie
