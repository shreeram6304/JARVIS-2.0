import ast
import math
import operator

class SafeEvaluator:
    """
    Safely parses and evaluates mathematical expressions using AST (Abstract Syntax Tree).
    Prevents security vulnerabilities associated with raw eval().
    """

    OPERATORS = {
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

    FUNCTIONS = {
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'asin': math.asin,
        'acos': math.acos,
        'atan': math.atan,
        'sinh': math.sinh,
        'cosh': math.cosh,
        'tanh': math.tanh,
        'sqrt': math.sqrt,
        'cbrt': lambda x: math.pow(x, 1/3) if x >= 0 else -math.pow(-x, 1/3),
        'log': math.log10,
        'log10': math.log10,
        'log2': math.log2,
        'ln': math.log,
        'exp': math.exp,
        'abs': abs,
        'fact': math.factorial,
        'factorial': math.factorial,
        'rad': math.radians,
        'deg': math.degrees,
    }

    CONSTANTS = {
        'pi': math.pi,
        'PI': math.pi,
        'e': math.e,
        'E': math.e,
        'tau': math.tau,
        'phi': (1 + math.sqrt(5)) / 2,
    }

    def __init__(self, angle_mode='deg'):
        self.angle_mode = angle_mode.lower()

    def evaluate(self, expression: str):
        if not expression or not expression.strip():
            raise ValueError("Expression is empty")

        expr = self._preprocess(expression)

        try:
            tree = ast.parse(expr, mode='eval')
            result = self._eval_node(tree.body)
            
            if isinstance(result, complex):
                raise ValueError("Complex numbers are not supported")
                
            return result
        except SyntaxError:
            raise ValueError("Invalid syntax in expression")

    def _preprocess(self, expr: str) -> str:
        # Replace mathematical symbols with Python equivalents
        expr = expr.replace('×', '*').replace('÷', '/')
        expr = expr.replace('^', '**')
        expr = expr.replace('π', 'pi')
        expr = expr.replace('√', 'sqrt')
        
        # Handle implied multiplication like 2pi or 5(3+2)
        # Replacing simple patterns
        cleaned = []
        i = 0
        while i < len(expr):
            cleaned.append(expr[i])
            if i < len(expr) - 1:
                curr, nxt = expr[i], expr[i+1]
                if (curr.isdigit() and (nxt.isalpha() or nxt == '(')) or (curr == ')' and (nxt.isdigit() or nxt.isalpha() or nxt == '(')):
                    cleaned.append('*')
            i += 1
            
        return "".join(cleaned)

    def _eval_node(self, node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Only numbers are supported")

        elif isinstance(node, ast.Name):
            if node.id in self.CONSTANTS:
                return self.CONSTANTS[node.id]
            raise ValueError(f"Unknown variable or constant: '{node.id}'")

        elif isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type in self.OPERATORS:
                operand = self._eval_node(node.operand)
                return self.OPERATORS[op_type](operand)
            raise ValueError("Unsupported unary operator")

        elif isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type in self.OPERATORS:
                left = self._eval_node(node.left)
                right = self._eval_node(node.right)
                
                if op_type == ast.Div and right == 0:
                    raise ZeroDivisionError("Division by zero")
                if op_type == ast.Pow and abs(right) > 1000:
                    raise ValueError("Exponent too large")
                    
                return self.OPERATORS[op_type](left, right)
            raise ValueError("Unsupported binary operator")

        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                func_name = node.func.id.lower()
                if func_name in self.FUNCTIONS:
                    args = [self._eval_node(arg) for arg in node.args]
                    if not args:
                        raise ValueError(f"Function '{func_name}' requires parameters")

                    # Handle trigonometric mode conversions
                    if func_name in ('sin', 'cos', 'tan'):
                        if self.angle_mode == 'deg':
                            args[0] = math.radians(args[0])
                        res = self.FUNCTIONS[func_name](*args)
                        return res
                    elif func_name in ('asin', 'acos', 'atan'):
                        res = self.FUNCTIONS[func_name](*args)
                        if self.angle_mode == 'deg':
                            res = math.degrees(res)
                        return res

                    return self.FUNCTIONS[func_name](*args)
            raise ValueError("Unsupported function call")

        else:
            raise ValueError("Invalid expression element")