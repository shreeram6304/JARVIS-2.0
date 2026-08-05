"""
OmniCalc Core Engine Package.
Contains expression evaluation, unit conversion, and calculation history modules.
"""

from .evaluator import MathEvaluator
from .converter import UnitConverter
from .history import HistoryManager

__all__ = ["MathEvaluator", "UnitConverter", "HistoryManager"]