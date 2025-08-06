import unittest
from calculator import Calculator
import math


class ApplicationTest(unittest.TestCase):

    def test_add(self):
        for x, y, expected in [(1, 2, 3), (0, 0, 0), (-1, -2, -3),
                               (1.5, 2.5, 4.0), (1e10, -1e10, 0)]:
            self.assertEqual(Calculator.add(x, y), expected)
        self.assertRaises(TypeError, Calculator.add, '1', 2)
        # TypeError: can only concatenate str (not "int") to str
        pass

    def test_divide(self):
        for x, y, expected in [(6, 2, 3), (-6, 2, -3), (0, 1, 0),
                               (1, 3, 1/3), (1e10, 1e-10, 1e20)]:
            self.assertEqual(Calculator.divide(x, y), expected)
        self.assertRaises(ZeroDivisionError, Calculator.divide, 1, 0)
        # ZeroDivisionError: division by zero
        pass

    def test_sqrt(self):
        for x, expected in [(4, 2), (0, 0), (1, 1),
                            (1e10, 1e5), (1e-10, 1e-5)]:
            self.assertEqual(Calculator.sqrt(x), expected)
        self.assertRaises(ValueError, Calculator.sqrt, -1)
        # ValueError: math domain error
        pass

    def test_exp(self):
        for x, expected in [(0, 1), (1, math.e), (2, round(math.e ** 2, 14)),
                            (-1, 1/math.e), (-2, 1/math.e**2)]:
            self.assertEqual(Calculator.exp(x), expected)
        self.assertAlmostEqual(Calculator.exp(2), math.e ** 2)
        self.assertRaises(OverflowError, Calculator.exp, 1e10)
        # OverflowError: math range error
        pass


if __name__ == '__main__':
    unittest.main()
