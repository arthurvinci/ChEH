import unittest

from LWE.tests.lwe_test import TestLWE
from LWE.tests.utils_test import TestLWEUtils

if __name__ == '__main__':
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLWEUtils)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestLWE))

    unittest.TextTestRunner().run(suite)



