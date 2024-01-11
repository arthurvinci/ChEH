import unittest
from LWE.tests.utils import TestLWEUtils
from LWE.tests.lwe import TestLWE

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLWEUtils)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestLWE))

    unittest.TextTestRunner().run(suite)
