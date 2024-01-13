from sage.all import *

import unittest

from LWE.tests.lwe_test import TestLWE
from LWE.tests.utils_test import TestLWEUtils
from RLWE.tests.rlwe_tests import TestRLWE

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLWEUtils)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestLWE))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestRLWE))

    unittest.TextTestRunner().run(suite)
