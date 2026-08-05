import ast
import math
import operator
from decimal import Decimal, OverflowError as DecimalOverflowError
from typing import Union, Dict, Any

class CalculatorEngine:
    def __init__(self):
        self.allowed_operators = {
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
        
        self.allowed_functions: Dict[str, Any] = {
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "asin": math.asin,
            "acos": math.acos,
            "atan": math.atan,
            "sinh": math.sinh,
            "cosh": math.cosh,
            "tanh": math.tanh,
            "sqrt": math.sqrt,
            "cbrt": lambda x: math.pow(x, 1/3) if x >= 0 else -math.pow(-x, 1/3),
            "log": math.log,
            "log10": math.log10,
            "log2": math.log2,
            "exp": math.exp,
            "abs": abs,
            "ceil": math.ceil,
            "floor": math.floor,
            "round": round,
            "fact": math.factorial,
            "factorial": math.factorial,
            "rad": math.radians,
            "deg": math.degrees
        }
        
        self.constants = {
            "pi": math.pi,
            "e": math.e,
            "tau": math.tau,
            "phi": (1 + math.sqrt(5)) / 2
        }

    def _eval_node(self, node: ast.AST) -> Union[int, float]:
        if isinstance(node, ast.Expression):
            return self._eval_node(node.body)

        elif isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Invalid constant: {node.value}")

        elif isinstance(node, ast.Name):
            name_lower = node.id.lower()
            if name_lower in self.constants:
                return self.constants[name_lower]
            raise ValueError(f"Unknown variable or constant: {node.id}")

        elif isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type in self.allowed_operators:
                operand = self._eval_node(node.operand)
                return self.allowed_operators[op_type](operand)
            raise ValueError(f"Unsupported unary operator: {node.op}")

        elif isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type in self.allowed_operators:
                left = self._eval_node(node.left)
                right = self._eval_node(node.right)
                
                if op_type in (ast.Div, ast.FloorDiv, ast.Mod) and right == 0:
                    raise ZeroDivisionError("Division by zero is undefined.")
                
                if op_type == ast.Pow and left < 0 and isinstance(right, float) and not right.is_integer():
                    raise ValueError("Complex numbers are not supported.")

                if op_type == ast.Pow and right > 1000:
                    raise ValueError("Exponent too large.")
                    
                return self.allowed_operators[op_type](left, right)
            raise ValueError(f"Unsupported binary operator: {node.op}")

        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Function calls must be direct identifier names.")
            
            func_name = node.func.id.lower()
            if func_name not in self.allowed_functions:
                raise ValueError(f"Unsupported function: {node.func.id}")

            args = [self._eval_node(arg) for arg in node.args]
            func = self.allowed_functions[func_name]
            
            try:
                return func(*args)
            except TypeError:
                raise ValueError(f"Incorrect number of arguments for '{func_name}'.")
            except ValueError as e:
                raise ValueError(f"Domain error in '{func_name}': {str(e)}")

        else:
            raise ValueError(f"Unsupported expression syntax.")

    def evaluate(self, expression: str) -> Union[int, float]:
        if not expression or not expression.strip():
            raise ValueError("Expression is empty.")

        sanitized = expression.strip()
        sanitized = sanitized.replace("×", "*").replace("÷", "/").replace("−", "-").replace("π", "pi")
        sanitized = sanitized.replace("^", "**")

        try:
            parsed_ast = ast.parse(sanitized, mode='eval')
            result = self._eval_node(parsed_ast)
            
            if isinstance(result, float):
                if math.isnan(result) or math.isinf(result):
                    raise ValueError("Result is infinite or undefined.")
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)

            return result
        except SyntaxError:
            raise ValueError("Invalid mathematical syntax.")
        except OverflowError:
            raise ValueError("Calculation resulted in numerical overflow.")
        except DecimalOverflowError:
            raise ValueError("Number exceeds max float precision limit.")