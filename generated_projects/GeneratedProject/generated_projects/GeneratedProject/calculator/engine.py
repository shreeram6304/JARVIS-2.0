import ast
import math
import operator
from typing import Union, Dict, Any, Callable

class MathEngineError(Exception):
    """Custom exception for math evaluation errors."""
    pass

class SafeMathEvaluator:
    """
    Evaluates mathematical expressions safely using Python AST parsing.
    Prevents arbitrary code execution by restricting nodes to basic math operations.
    """

    ALLOWED_OPERATORS: Dict[type, Callable] = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    ALLOWED_FUNCTIONS: Dict[str, Callable] = {
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "asin": math.asin,
        "acos": math.acos,
        "atan": math.atan,
        "sqrt": math.sqrt,
        "log": math.log10,
        "ln": math.log,
        "exp": math.exp,
        "abs": abs,
        "factorial": math.factorial,
        "rad": math.radians,
        "deg": math.degrees,
    }

    ALLOWED_CONSTANTS: Dict[str, Union[int, float]] = {
        "pi": math.pi,
        "e": math.e,
        "PI": math.pi,
        "E": math.e,
    }

    MAX_POWER = 1000  # Prevent CPU exhaustion via exponentiation DoS

    def __init__(self) -> None:
        pass

    def evaluate(self, expression: str) -> Union[int, float]:
        """
        Parses and evaluates a math expression string.
        Returns calculated numeric result or raises MathEngineError.
        """
        if not expression or not expression.strip():
            raise MathEngineError("Expression is empty")

        cleaned_expr = self._preprocess_expression(expression)

        try:
            tree = ast.parse(cleaned_expr, mode="eval")
            result = self._eval_node(tree.body)

            if isinstance(result, complex):
                raise MathEngineError("Complex numbers are not supported")

            # Check if result is infinite or NaN
            if math.isinf(result):
                raise MathEngineError("Result resulted in infinity (Overflow)")
            if math.isnan(result):
                raise MathEngineError("Result is undefined (NaN)")

            # Format whole floats as integers cleanly
            if isinstance(result, float) and result.is_integer():
                return int(result)

            return round(result, 10)

        except SyntaxError:
            raise MathEngineError("Invalid expression syntax")
        except ZeroDivisionError:
            raise MathEngineError("Division by zero")
        except OverflowError:
            raise MathEngineError("Number overflow")
        except ValueError as e:
            raise MathEngineError(f"Mathematical error: {str(e)}")
        except MathEngineError:
            raise
        except Exception as e:
            raise MathEngineError(f"Evaluation error: {str(e)}")

    def _preprocess_expression(self, expr: str) -> str:
        """Standardize visual symbols to Python syntax."""
        expr = expr.replace("×", "*").replace("÷", "/")
        expr = expr.replace("−", "-").replace("π", "pi")
        expr = expr.replace("^", "**")
        return expr

    def _eval_node(self, node: ast.AST) -> Union[int, float]:
        """Recursively evaluates AST nodes."""
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise MathEngineError(f"Invalid constant type: {type(node.value)}")

        # Compatibility with older Python AST AST.Num
        if isinstance(node, ast.Num):
            return node.n

        if isinstance(node, ast.Name):
            if node.id in self.ALLOWED_CONSTANTS:
                return self.ALLOWED_CONSTANTS[node.id]
            raise MathEngineError(f"Unknown variable or constant: '{node.id}'")

        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type in self.ALLOWED_OPERATORS:
                operand = self._eval_node(node.operand)
                return self.ALLOWED_OPERATORS[op_type](operand)
            raise MathEngineError(f"Unsupported unary operator: {node.op}")

        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type in self.ALLOWED_OPERATORS:
                left = self._eval_node(node.left)

                # Exponentiation safety limits
                if op_type == ast.Pow:
                    right = self._eval_node(node.right)
                    if right > self.MAX_POWER:
                        raise MathEngineError(f"Exponent exceeds maximum allowed limit ({self.MAX_POWER})")
                    return self.ALLOWED_OPERATORS[op_type](left, right)

                right = self._eval_node(node.right)
                return self.ALLOWED_OPERATORS[op_type](left, right)
            raise MathEngineError(f"Unsupported binary operator: {node.op}")

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise MathEngineError("Function calls must be direct identifier names")
            
            func_name = node.func.id
            if func_name not in self.ALLOWED_FUNCTIONS:
                raise MathEngineError(f"Unsupported function: '{func_name}'")

            args = [self._eval_node(arg) for arg in node.args]
            try:
                return self.ALLOWED_FUNCTIONS[func_name](*args)
            except Exception as e:
                raise MathEngineError(f"Error executing '{func_name}': {str(e)}")

        raise MathEngineError(f"Unsupported syntax: {type(node).__name__}")