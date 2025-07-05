# tests.py

import unittest
from pkg.calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_addition(self):
        result = self.calculator.evaluate("3 + 5")
        self.assertEqual(result, 8)

    def test_subtraction(self):
        result = self.calculator.evaluate("10 - 4")
        self.assertEqual(result, 6)

    def test_multiplication(self):
        result = self.calculator.evaluate("3 * 4")
        self.assertEqual(result, 12)

    def test_division(self):
        result = self.calculator.evaluate("10 / 2")
        self.assertEqual(result, 5)

    def test_nested_expression(self):
        result = self.calculator.evaluate("3 * 4 + 5")
        self.assertEqual(result, 17)

    def test_complex_expression(self):
        result = self.calculator.evaluate("2 * 3 - 8 / 2 + 5")
        self.assertEqual(result, 7)

    def test_empty_expression(self):
        result = self.calculator.evaluate("")
        self.assertIsNone(result)

    def test_invalid_operator(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("$ 3 5")

    def test_not_enough_operands(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("+ 3")

    def test_negative_numbers(self):
        self.assertEqual(self.calculator.evaluate("-5 + 2"), -3)
        self.assertEqual(self.calculator.evaluate("3 * -4"), -12)

    def test_decimal_numbers(self):
        self.assertEqual(self.calculator.evaluate("2.5 + 3.5"), 6)
        self.assertEqual(self.calculator.evaluate("7.0 / 2.0"), 3.5)

    def test_division_by_zero(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("5 / 0")


if __name__ == "__main__":
    unittest.main()