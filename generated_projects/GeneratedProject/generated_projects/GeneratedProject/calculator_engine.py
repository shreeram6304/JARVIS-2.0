import ast
import math
import operator
from typing import Union, Dict, Any

class CalculationError(Exception):
    """Custom exception for math calculation errors."""
    pass

class SafeCalculatorEngine:
    """
    Safely evaluates mathematical expressions using Python's AST parser.
    Prevents security vulnerabilities associated with eval().
    """

    # Allowed unary operators
    UNARY_OPERATORS = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    # Allowed binary operators
    BINARY_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }

    # Allowed math functions
    MATH_FUNCTIONS = {
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'asin': math.asin,
        'acos': math.acos,
        'atan': math.atan,
        'sqrt': math.sqrt,
        'log': math.log,
        'log10': math.log10,
        'exp': math.exp,
        'abs': abs,
        'ceil': math.ceil,
        'floor': math.floor,
        'round': round,
        'factorial': math.factorial,
        'rad': math.radians,
        'deg': math.degrees,
    }

    # Allowed mathematical constants
    MATH_CONSTANTS = {
        'pi': math.pi,
        'e': math.e,
        'tau': math.tau,
        'inf': math.inf,
    }

    def __init__(self, max_power: float = 10000.0):
        self.max_power = max_power

    def evaluate(self, expression: str) -> Union[int, float]:
        """
        Parse and evaluate a math expression string safely.
        """
        if not expression or not expression.strip():
            raise CalculationError("Empty expression")

        # Preprocess expression (convert visual operators to python operators)
        clean_expr = expression.replace('×', '*').replace('÷', '/').replace('^', '**').replace('π', 'pi')

        try:
            parsed_ast = ast.parse(clean_expr, mode='eval')
            return self._eval_node(parsed_ast.body)
        except SyntaxError:
            raise CalculationError("Invalid mathematical expression syntax")
        except ZeroDivisionError:
            raise CalculationError("Division by zero is undefined")
        except OverflowError:
            raise CalculationError("Result exceeded maximum numerical capacity")
        except ValueError as ve:
            raise CalculationError(f"Math domain error: {str(ve)}")
        except Exception as e:
            raise CalculationError(f"Evaluation error: {str(e)}")

    def _eval_node(self, node: ast.AST) -> Union[int, float]:
        """Recursively traverse AST and evaluate nodes."""
        if isinstance(node, ast.Constant):  # Numbers/Constants in Python 3.8+
            if isinstance(node.value, (int, float)):
                return node.value
            raise CalculationError(f"Unsupported constant type: {type(node.value).__name__}")

        elif isinstance(node, ast.Name):
            if node.id in self.MATH_CONSTANTS:
                return self.MATH_CONSTANTS[node.id]
            raise CalculationError(f"Unknown variable or constant: '{node.id}'")

        elif isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type in self.UNARY_OPERATORS:
                operand = self._eval_node(node.operand)
                return self.UNARY_OPERATORS[op_type](operand)
            raise CalculationError(f"Unsupported unary operator: {op_type.__name__}")

        elif isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type in self.BINARY_OPERATORS:
                left = self._eval_node(node.left)
                right = self._eval_node(node.right)

                # Guard against huge power computations preventing CPU exhaustion
                if op_type == ast.Pow:
                    if abs(right) > 1000 or (isinstance(left, (int, float)) and abs(left) > 1000 and right > 100):
                        raise CalculationError("Exponent power value too large")

                return self.BINARY_OPERATORS[op_type](left, right)
            raise CalculationError(f"Unsupported binary operator: {op_type.__name__}")

        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise CalculationError("Complex function calls are not supported")
            
            func_name = node.func.id
            if func_name not in self.MATH_FUNCTIONS:
                raise CalculationError(f"Unsupported function: '{func_name}'")

            args = [self._eval_node(arg) for arg in node.args]
            func = self.MATH_FUNCTIONS[func_name]

            try:
                return func(*args)
            except Exception as e:
                raise CalculationError(f"Error in function '{func_name}': {str(e)}")

        else:
            raise CalculationError(f"Unsupported language construct: {type(node).__name__}")

    @staticmethod
    def format_result(val: Union[int, float]) -> str:
        """Formats numbers cleanly, eliminating redundant trailing decimals."""
        if isinstance(val, float):
            if val.is_integer():
                return str(int(val))
            # Format to maximum 10 decimal places to prevent float precision noise
            return f"{round(val, 10):.10g}"
        return str(val)


class UnitConverter:
    """Handles unit conversion calculations across diverse physical domains."""

    CONVERSIONS: Dict[str, Dict[str, float]] = {
        'length': {
            'mm': 0.001,
            'cm': 0.01,
            'm': 1.0,
            'km': 1000.0,
            'in': 0.0254,
            'ft': 0.3048,
            'yd': 0.9144,
            'mi': 1609.344
        },
        'weight': {
            'mg': 0.000001,
            'g': 0.001,
            'kg': 1.0,
            'ton': 1000.0,
            'oz': 0.028349523125,
            'lb': 0.45359237
        },
        'area': {
            'sq_m': 1.0,
            'sq_km': 1000000.0,
            'sq_ft': 0.09290304,
            'acre': 4046.8564224,
            'hectare': 10000.0
        },
        'volume': {
            'ml': 0.001,
            'l': 1.0,
            'cu_m': 1000.0,
            'tsp': 0.00492892,
            'tbsp': 0.0147868,
            'cup': 0.240,
            'gal': 3.78541
        }
    }

    @classmethod
    def convert(cls, category: str, from_unit: str, to_unit: str, value: float) -> float:
        category = category.lower()
        if category == 'temperature':
            return cls._convert_temperature(from_unit, to_unit, value)

        if category not in cls.CONVERSIONS:
            raise ValueError(f"Invalid conversion category: '{category}'")

        units = cls.CONVERSIONS[category]
        if from_unit not in units or to_unit not in units:
            raise ValueError(f"Invalid units for category {category}: '{from_unit}' -> '{to_unit}'")

        # Convert to base standard metric unit then to target unit
        base_val = value * units[from_unit]
        return base_val / units[to_unit]

    @staticmethod
    def _convert_temperature(from_u: str, to_u: str, val: float) -> float:
        from_u = from_u.lower()
        to_u = to_u.lower()

        # Normalize to Celsius
        if from_u in ['c', 'celsius']:
            celsius = val
        elif from_u in ['f', 'fahrenheit']:
            celsius = (val - 32) * 5 / 9
        elif from_u in ['k', 'kelvin']:
            celsius = val - 273.15
        else:
            raise ValueError(f"Unknown temperature unit: '{from_u}'")

        # Convert Celsius to target
        if to_u in ['c', 'celsius']:
            return celsius
        elif to_u in ['f', 'fahrenheit']:
            return (celsius * 9 / 5) + 32
        elif to_u in ['k', 'kelvin']:
            return celsius + 273.15
        else:
            raise ValueError(f"Unknown temperature unit: '{to_u}'")