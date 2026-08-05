import ast
import math
import operator
from typing import Union, Dict, Any, Callable

class MathEvaluator:
    """
    Safely parses and evaluates mathematical expressions using Python AST.
    """
    
    # Allowed operators
    OPERATORS: Dict[type, Callable[..., Any]] = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    # Allowed functions
    FUNCTIONS: Dict[str, Callable[..., Any]] = {
        "sin": lambda x: math.sin(math.radians(x)),
        "cos": lambda x: math.cos(math.radians(x)),
        "tan": lambda x: math.tan(math.radians(x)),
        "asin": lambda x: math.degrees(math.asin(x)),
        "acos": lambda x: math.degrees(math.acos(x)),
        "atan": lambda x: math.degrees(math.atan(x)),
        "sqrt": math.sqrt,
        "log": math.log10,
        "ln": math.log,
        "abs": abs,
        "fact": lambda x: math.factorial(int(x)),
        "exp": math.exp,
    }

    # Allowed constants
    CONSTANTS: Dict[str, float] = {
        "pi": math.pi,
        "e": math.e,
        "TAU": math.tau,
    }

    @classmethod
    def evaluate(cls, expression: str) -> Union[int, float]:
        """
        Evaluates a string math expression safely.
        Raises ValueError or ZeroDivisionError on invalid syntax/math errors.
        """
        if not expression or not expression.strip():
            raise ValueError("Expression is empty.")

        # Replace user friendly symbols
        cleaned_expr = (
            expression.replace("×", "*")
            .replace("÷", "/")
            .replace("π", "pi")
            .replace("^", "**")
            .strip()
        )

        try:
            tree = ast.parse(cleaned_expr, mode="eval")
            return cls._eval_node(tree.body)
        except SyntaxError as e:
            raise ValueError("Invalid mathematical syntax.") from e
        except ZeroDivisionError:
            raise ZeroDivisionError("Division by zero is undefined.")
        except Exception as e:
            raise ValueError(str(e)) from e

    @classmethod
    def _eval_node(cls, node: ast.AST) -> Union[int, float]:
        if isinstance(node, ast.Constant):  # Numbers
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value)}")

        elif isinstance(node, ast.Name):  # Constants like pi, e
            if node.id in cls.CONSTANTS:
                return cls.CONSTANTS[node.id]
            raise ValueError(f"Unknown variable: {node.id}")

        elif isinstance(node, ast.BinOp):  # Binary operations (+, -, *, /, ^, %)
            left = cls._eval_node(node.left)
            right = cls._eval_node(node.right)
            op_type = type(node.op)
            
            if op_type in cls.OPERATORS:
                if op_type == ast.Div and right == 0:
                    raise ZeroDivisionError("Division by zero.")
                if op_type == ast.Pow and abs(left) > 1000 and right > 100:
                    raise ValueError("Overflow error in exponentiation.")
                return cls.OPERATORS[op_type](left, right)
            raise ValueError(f"Unsupported operator: {op_type.__name__}")

        elif isinstance(node, ast.UnaryOp):  # Unary operations (-x, +x)
            operand = cls._eval_node(node.operand)
            op_type = type(node.op)
            if op_type in cls.OPERATORS:
                return cls.OPERATORS[op_type](operand)
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

        elif isinstance(node, ast.Call):  # Function calls (sin(x), sqrt(x))
            if not isinstance(node.func, ast.Name):
                raise ValueError("Invalid function call signature.")
            
            func_name = node.func.id
            if func_name not in cls.FUNCTIONS:
                raise ValueError(f"Function '{func_name}' is not supported.")

            args = [cls._eval_node(arg) for arg in node.args]
            return cls.FUNCTIONS[func_name](*args)

        else:
            raise ValueError(f"Unsupported expression structure: {type(node).__name__}")