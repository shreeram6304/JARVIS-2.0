import ast
import math
import operator
from typing import Dict, Any, Union

class MathEngine:
    """Safe AST-based mathematical expression evaluator."""

    def __init__(self):
        # Allowed operators
        self.operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.FloorDiv: operator.floordiv,
            ast.Mod: operator.mod,
            ast.Pow: operator.pow,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos,
        }

        # Safe Math constants
        self.constants = {
            'pi': math.pi,
            'e': math.e,
            'tau': math.tau if hasattr(math, 'tau') else math.pi * 2,
            'phi': (1 + math.sqrt(5)) / 2,
            'inf': math.inf
        }

    def _get_math_functions(self, angle_mode: str) -> Dict[str, Any]:
        """Generate mathematical functions adjusted for DEG/RAD mode."""

        def _to_rad(val: float) -> float:
            return math.radians(val) if angle_mode == 'DEG' else val

        def _from_rad(val: float) -> float:
            return math.degrees(val) if angle_mode == 'DEG' else val

        return {
            # Trigonometric functions
            'sin': lambda x: math.sin(_to_rad(x)),
            'cos': lambda x: math.cos(_to_rad(x)),
            'tan': lambda x: math.tan(_to_rad(x)),
            'asin': lambda x: _from_rad(math.asin(x)),
            'acos': lambda x: _from_rad(math.acos(x)),
            'atan': lambda x: _from_rad(math.atan(x)),
            'sinh': math.sinh,
            'cosh': math.cosh,
            'tanh': math.tanh,
            'asinh': math.asinh,
            'acosh': math.acosh,
            'atanh': math.atanh,

            # General mathematical functions
            'sqrt': math.sqrt,
            'cbrt': lambda x: x ** (1.0 / 3.0) if x >= 0 else -((-x) ** (1.0 / 3.0)),
            'abs': abs,
            'ceil': math.ceil,
            'floor': math.floor,
            'round': round,
            'exp': math.exp,
            'log': math.log,         # Natural log
            'ln': math.log,          # Alias for natural log
            'log10': math.log10,     # Log base 10
            'log2': math.log2,       # Log base 2
            'fact': lambda x: math.factorial(int(x)),
            'factorial': lambda x: math.factorial(int(x)),
            'rad': math.radians,
            'deg': math.degrees
        }

    def _eval_node(self, node: ast.AST, funcs: Dict[str, Any]) -> Union[int, float]:
        """Recursively evaluate an AST node safely."""
        if isinstance(node, ast.Constant):  # Python 3.8+ for numbers/constants
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

        elif isinstance(node, ast.Name):
            # Identifiers like pi, e, or function names
            name = node.id.lower()
            if name in self.constants:
                return self.constants[name]
            raise ValueError(f"Unknown variable or constant '{node.id}'")

        elif isinstance(node, ast.BinOp):
            left = self._eval_node(node.left, funcs)
            right = self._eval_node(node.right, funcs)
            op_type = type(node.op)
            if op_type in self.operators:
                if op_type in (ast.Div, ast.FloorDiv, ast.Mod) and right == 0:
                    raise ZeroDivisionError("Division by zero")
                # Limit exponential power to prevent CPU exhaustion DoS
                if op_type == ast.Pow:
                    if abs(right) > 10000 or (isinstance(left, (int, float)) and abs(left) > 100 and right > 1000):
                        raise ValueError("Exponent too large")
                return self.operators[op_type](left, right)
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

        elif isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand, funcs)
            op_type = type(node.op)
            if op_type in self.operators:
                return self.operators[op_type](operand)
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Nested function calls must use explicit names")
            func_name = node.func.id.lower()
            if func_name not in funcs:
                raise ValueError(f"Unknown function '{node.func.id}'")

            args = [self._eval_node(arg, funcs) for arg in node.args]
            return funcs[func_name](*args)

        else:
            raise ValueError(f"Unsupported mathematical syntax: {type(node).__name__}")

    def evaluate(self, expression: str, angle_mode: str = 'DEG') -> Dict[str, Any]:
        """
        Parse and evaluate a math string safely.
        Returns dictionary with result or error message.
        """
        if not expression or not expression.strip():
            return {'status': 'error', 'message': 'Expression is empty'}

        # Preprocess expression
        cleaned = expression.replace('×', '*').replace('÷', '/').replace('^', '**').replace('π', 'pi')
        cleaned = cleaned.strip()

        funcs = self._get_math_functions(angle_mode)

        try:
            parsed = ast.parse(cleaned, mode='eval')
            raw_result = self._eval_node(parsed.body, funcs)

            if isinstance(raw_result, complex):
                return {'status': 'error', 'message': 'Complex number results not supported'}

            if math.isnan(raw_result):
                return {'status': 'error', 'message': 'Undefined result (NaN)'}

            if math.isinf(raw_result):
                return {'status': 'error', 'message': 'Result is infinite (Overflow)'}

            # Format result
            if isinstance(raw_result, float) and raw_result.is_integer():
                formatted = str(int(raw_result))
                val = int(raw_result)
            else:
                # Round to reasonable scientific precision (10 decimal places)
                val = round(raw_result, 10)
                formatted = f"{val:g}"

            # Check if scientific mode was triggered (used functions/constants)
            is_sci = any(fn in cleaned.lower() for fn in funcs.keys()) or any(c in cleaned.lower() for c in self.constants)

            return {
                'status': 'success',
                'result': val,
                'formatted_result': formatted,
                'is_scientific': is_sci
            }

        except ZeroDivisionError:
            return {'status': 'error', 'message': 'Cannot divide by zero'}
        except ValueError as ve:
            return {'status': 'error', 'message': str(ve)}
        except SyntaxError:
            return {'status': 'error', 'message': 'Invalid mathematical syntax'}
        except Exception as e:
            return {'status': 'error', 'message': f"Calculation error: {str(e)}"}