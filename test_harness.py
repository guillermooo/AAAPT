# Sample test harness. It does not actually test anything meaningful in AAPT.

from AAAPT.runner import register_tests


TESTS_SOME_FEATURE_A = 'AAAPT.tests.test_sample'

TESTS_ALL_FEATURE_A = [TESTS_SOME_FEATURE_A]

test_suites = {
    'feata': TESTS_ALL_FEATURE_A,
}


register_tests(test_suites)

