import unittest
import math
from calculator.engine import SafeEvaluator
from calculator.history import HistoryManager
from app import app

class TestSafeEvaluator(unittest.TestCase):
    def setUp(self):
        self.evaluator = SafeEvaluator()

    def test_basic_arithmetic(self):
        self.assertEqual(self.evaluator.evaluate("2 + 3"), 5)
        self.assertEqual(self.evaluator.evaluate("10 - 4"), 6)
        self.assertEqual(self.evaluator.evaluate("3 * 4"), 12)
        self.assertEqual(self.evaluator.evaluate("15 / 3"), 5)
        self.assertEqual(self.evaluator.evaluate("10 % 3"), 1)
        self.assertEqual(self.evaluator.evaluate("2 ^ 3"), 8)

    def test_unicode_and_shorthand_symbols(self):
        self.assertEqual(self.evaluator.evaluate("6 × 7"), 42)
        self.assertEqual(self.evaluator.evaluate("20 ÷ 4"), 5)
        self.assertEqual(self.evaluator.evaluate("10 − 3"), 7)
        self.assertAlmostEqual(self.evaluator.evaluate("π"), math.pi)

    def test_trigonometry_deg_and_rad(self):
        self.assertAlmostEqual(self.evaluator.evaluate("sin(90)", angle_unit="deg"), 1.0)
        self.assertAlmostEqual(self.evaluator.evaluate("cos(0)", angle_unit="deg"), 1.0)
        self.assertAlmostEqual(self.evaluator.evaluate("sin(pi/2)", angle_unit="rad"), 1.0)

    def test_advanced_functions(self):
        self.assertEqual(self.evaluator.evaluate("sqrt(16)"), 4)
        self.assertEqual(self.evaluator.evaluate("5!"), 120)
        self.assertEqual(self.evaluator.evaluate("abs(-25)"), 25)
        self.assertAlmostEqual(self.evaluator.evaluate("ln(e)"), 1.0)
        self.assertAlmostEqual(self.evaluator.evaluate("log10(100)"), 2.0)

    def test_errors(self):
        with self.assertRaises(ZeroDivisionError):
            self.evaluator.evaluate("10 / 0")
        with self.assertRaises(ValueError):
            self.evaluator.evaluate("sqrt(-4)")
        with self.assertRaises(ValueError):
            self.evaluator.evaluate("import os")

class TestHistoryManager(unittest.TestCase):
    def setUp(self):
        self.history = HistoryManager(max_size=3)

    def test_add_and_retrieve_history(self):
        self.history.add_entry("2+2", "4")
        self.history.add_entry("3+3", "6")
        items = self.history.get_history()
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["expression"], "3+3")

    def test_max_size_limit(self):
        for i in range(5):
            self.history.add_entry(f"{i}+{i}", str(i*2))
        items = self.history.get_history()
        self.assertEqual(len(items), 3)

    def test_clear_history(self):
        self.history.add_entry("1+1", "2")
        self.history.clear()
        self.assertEqual(len(self.history.get_history()), 0)

class TestFlaskAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_calculate_endpoint(self):
        response = self.client.post('/api/calculate', json={
            "expression": "10 + 5 * 2",
            "angle_unit": "deg"
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["result"], "20")

    def test_invalid_expression_endpoint(self):
        response = self.client.post('/api/calculate', json={
            "expression": "10 / 0",
            "angle_unit": "deg"
        })
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()