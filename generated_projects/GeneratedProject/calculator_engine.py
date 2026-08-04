import ast
import math
import operator
from typing import Union, Dict, Any

class SafeEvaluator:
    """
    AST-based safe evaluator for mathematical expressions.
    Prevents execution of arbitrary Python code.
    """
    
    ALLOWED_OPERATORS = {
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

    ALLOWED_FUNCTIONS = {
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'asin': math.asin,
        'acos': math.acos,
        'atan': math.atan,
        'sinh': math.sinh,
        'cosh': math.cosh,
        'tanh': math.tanh,
        'log': math.log,
        'log10': math.log10,
        'ln': math.log,
        'sqrt': math.sqrt,
        'cbrt': lambda x: x ** (1.0 / 3.0),
        'abs': abs,
        'fact': math.factorial,
        'factorial': math.factorial,
        'rad': math.radians,
        'deg': math.degrees,
        'exp': math.exp
    }

    ALLOWED_CONSTANTS = {
        'pi': math.pi,
        'e': math.e,
        'tau': math.tau,
        'phi': (1 + 5 ** 0.5) / 2
    }

    def __init__(self, angle_mode: str = 'rad'):
        self.angle_mode = angle_mode.lower()

    def _eval_node(self, node: ast.AST) -> Union[int, float]:
        if isinstance(node, ast.Expression):
            return self._eval_node(node.body)
        
        elif isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Invalid constant type: {type(node.value).__name__}")
        
        elif isinstance(node, ast.Num):  # Fallback for Python < 3.8 AST
            return node.n
        
        elif isinstance(node, ast.Name):
            if node.id in self.ALLOWED_CONSTANTS:
                return self.ALLOWED_CONSTANTS[node.id]
            raise ValueError(f"Undefined variable or constant: '{node.id}'")
        
        elif isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type in self.ALLOWED_OPERATORS:
                operand = self._eval_node(node.operand)
                return self.ALLOWED_OPERATORS[op_type](operand)
            raise ValueError(f"Unsupported unary operator: {node.op}")
        
        elif isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type in self.ALLOWED_OPERATORS:
                left = self._eval_node(node.left)
                right = self._eval_node(node.right)
                
                if op_type in (ast.Div, ast.FloorDiv, ast.Mod) and right == 0:
                    raise ZeroDivisionError("Division by zero")
                
                if op_type == ast.Pow and left < 0 and isinstance(right, float) and not right.is_integer():
                    raise ValueError("Complex numbers resulting from fractional power of negative base are not supported")
                
                res = self.ALLOWED_OPERATORS[op_type](left, right)
                if isinstance(res, complex):
                    raise ValueError("Complex number result not supported")
                return res
            raise ValueError(f"Unsupported binary operator: {node.op}")
        
        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Invalid function call signature")
            
            func_name = node.func.id.lower()
            if func_name not in self.ALLOWED_FUNCTIONS:
                raise ValueError(f"Unsupported function: '{func_name}'")
            
            args = [self._eval_node(arg) for arg in node.args]
            
            # Handle angle modes for trigonometric functions
            if self.angle_mode == 'deg' and func_name in ('sin', 'cos', 'tan'):
                args[0] = math.radians(args[0])
            
            try:
                result = self.ALLOWED_FUNCTIONS[func_name](*args)
                if self.angle_mode == 'deg' and func_name in ('asin', 'acos', 'atan'):
                    result = math.degrees(result)
                return result
            except ValueError as ve:
                raise ValueError(f"Math domain error in {func_name}(): {str(ve)}")
            except OverflowError:
                raise ValueError("Numeric overflow")
        
        else:
            raise ValueError(f"Unsupported syntax construct: {type(node).__name__}")

    def evaluate(self, expression: str) -> Dict[str, Any]:
        """
        Clean, parse and evaluate mathematical string expression.
        """
        if not expression or not expression.strip():
            raise ValueError("Expression is empty")
        
        cleaned = expression.strip()
        cleaned = cleaned.replace('×', '*').replace('÷', '/').replace('−', '-')
        cleaned = cleaned.replace('π', 'pi').replace('√', 'sqrt')
        cleaned = cleaned.replace('^', '**')

        try:
            parsed = ast.parse(cleaned, mode='eval')
            result = self._eval_node(parsed)
            
            # Formatting floats
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
            
            return {
                "success": True,
                "expression": expression,
                "result": result
            }
        except SyntaxError:
            raise ValueError("Invalid syntax in expression")
        except ZeroDivisionError:
            raise ValueError("Division by zero")