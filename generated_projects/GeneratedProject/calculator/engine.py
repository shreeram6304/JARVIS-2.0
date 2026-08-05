import ast
import math
import operator as op

class SafeMathEngine:
    OPERATORS = {
        ast.Add: op.add,
        ast.Sub: op.sub,
        ast.Mult: op.mul,
        ast.Div: op.truediv,
        ast.Pow: op.pow,
        ast.Mod: op.mod,
        ast.USub: op.neg,
        ast.UAdd: op.pos,
    }

    FUNCTIONS = {
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'asin': math.asin,
        'acos': math.acos,
        'atan': math.atan,
        'sqrt': math.sqrt,
        'log': math.log10,
        'ln': math.log,
        'abs': abs,
        'factorial': lambda x: math.factorial(int(x)),
        'deg': math.degrees,
        'rad': math.radians,
    }

    CONSTANTS = {
        'pi': math.pi,
        'e': math.e,
        'PI': math.pi,
        'E': math.e,
    }

    @classmethod
    def evaluate(cls, expression: str) -> float:
        if not expression or not expression.strip():
            raise ValueError("Expression cannot be empty")
        
        # Sanitize and normalize string
        cleaned_expr = (
            expression.replace('×', '*')
            .replace('÷', '/')
            .replace('^', '**')
            .replace('π', 'pi')
        )
        
        try:
            parsed_tree = ast.parse(cleaned_expr, mode='eval')
            result = cls._eval_node(parsed_tree.body)
            return float(result)
        except ZeroDivisionError:
            raise ValueError("Error: Division by zero")
        except Exception as e:
            raise ValueError(f"Invalid Expression: {str(e)}")

    @classmethod
    def _eval_node(cls, node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return float(node.value)
            raise ValueError("Unsupported constant type")
            
        elif isinstance(node, ast.Name):
            if node.id in cls.CONSTANTS:
                return cls.CONSTANTS[node.id]
            raise ValueError(f"Unknown constant or variable '{node.id}'")
            
        elif isinstance(node, ast.BinOp):
            left = cls._eval_node(node.left)
            right = cls._eval_node(node.right)
            op_type = type(node.op)
            if op_type in cls.OPERATORS:
                if op_type == ast.Div and right == 0:
                    raise ZeroDivisionError("Division by zero")
                return cls.OPERATORS[op_type](left, right)
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
            
        elif isinstance(node, ast.UnaryOp):
            operand = cls._eval_node(node.operand)
            op_type = type(node.op)
            if op_type in cls.OPERATORS:
                return cls.OPERATORS[op_type](operand)
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
            
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in cls.FUNCTIONS:
                args = [cls._eval_node(arg) for arg in node.args]
                return cls.FUNCTIONS[node.func.id](*args)
            raise ValueError("Unsupported function call")
            
        else:
            raise ValueError("Invalid mathematical syntax")