import math
import pytest
from calculator.evaluator import SafeEvaluator

def test_basic_arithmetic():
    evaluator = SafeEvaluator()
    assert evaluator.evaluate("2 + 2") == 4
    assert evaluator.evaluate("10 - 4") == 6
    assert evaluator.evaluate("3 * 5") == 15
    assert evaluator.evaluate("20 / 4") == 5

def test_operator_precedence():
    evaluator = SafeEvaluator()
    assert evaluator.evaluate("2 + 3 * 4") == 14
    assert evaluator.evaluate("(2 + 3) * 4") == 20

def test_trigonometry():
    evaluator_deg = SafeEvaluator(angle_mode='deg')
    assert math.isclose(evaluator_deg.evaluate("sin(90)"), 1.0, abs_tol=1e-5)
    
    evaluator_rad = SafeEvaluator(angle_mode='rad')
    assert math.isclose(evaluator_rad.evaluate("sin(pi / 2)"), 1.0, abs_tol=1e-5)

def test_constants():
    evaluator = SafeEvaluator()
    assert math.isclose(evaluator.evaluate("pi"), math.pi)
    assert math.isclose(evaluator.evaluate("e"), math.e)

def test_division_by_zero():
    evaluator = SafeEvaluator()
    with pytest.raises(ZeroDivisionError):
        evaluator.evaluate("10 / 0")

def test_invalid_syntax():
    evaluator = SafeEvaluator()
    with pytest.raises(ValueError):
        evaluator.evaluate("2 ++ 3 **")