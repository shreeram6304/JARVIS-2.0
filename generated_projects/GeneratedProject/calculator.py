import ast
import math
import operator

class SafeEvaluator:
    """Safe AST-based mathematical expression evaluator."""
    
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
        'sqrt': math.sqrt,
        'log': math.log10,
        'ln': math.log,
        'exp': math.exp,
        'abs': abs,
        'ceil': math.ceil,
        'floor': math.floor,
        'fact': math.factorial,
        'factorial': math.factorial,
        'radians': math.radians,
        'degrees': math.degrees,
    }

    ALLOWED_NAMES = {
        'pi': math.pi,
        'e': math.e,
        'tau': math.tau,
    }

    @classmethod
    def evaluate(cls, expression: str, is_degree: bool = False) -> float:
        if not expression or not isinstance(expression, str):
            raise ValueError("Expression must be a non-empty string")

        # Sanitize and normalize expression
        clean_expr = expression.replace('×', '*').replace('÷', '/').replace('^', '**')
        clean_expr = clean_expr.replace('π', 'pi').replace('√', 'sqrt')
        
        try:
            tree = ast.parse(clean_expr, mode='eval')
            return cls._eval_node(tree.body, is_degree)
        except SyntaxError:
            raise ValueError("Invalid syntax in expression")

    @classmethod
    def _eval_node(cls, node, is_degree: bool):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return float(node.value)
            raise ValueError("Unsupported constant type")

        elif isinstance(node, ast.Name):
            name_lower = node.id.lower()
            if name_lower in cls.ALLOWED_NAMES:
                return cls.ALLOWED_NAMES[name_lower]
            raise ValueError(f"Unknown variable: {node.id}")

        elif isinstance(node, ast.BinOp):
            left = cls._eval_node(node.left, is_degree)
            right = cls._eval_node(node.right, is_degree)
            op_type = type(node.op)
            if op_type in cls.ALLOWED_OPERATORS:
                if op_type == ast.Div and right == 0:
                    raise ZeroDivisionError("Division by zero")
                return cls.ALLOWED_OPERATORS[op_type](left, right)
            raise ValueError(f"Unsupported operator: {op_type.__name__}")

        elif isinstance(node, ast.UnaryOp):
            operand = cls._eval_node(node.operand, is_degree)
            op_type = type(node.op)
            if op_type in cls.ALLOWED_OPERATORS:
                return cls.ALLOWED_OPERATORS[op_type](operand)
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Invalid function call")
            func_name = node.func.id.lower()
            if func_name not in cls.ALLOWED_FUNCTIONS:
                raise ValueError(f"Unsupported function: {func_name}")
            
            args = [cls._eval_node(arg, is_degree) for arg in node.args]
            
            if is_degree and func_name in ('sin', 'cos', 'tan'):
                args[0] = math.radians(args[0])

            res = cls.ALLOWED_FUNCTIONS[func_name](*args)

            if is_degree and func_name in ('asin', 'acos', 'atan'):
                res = math.degrees(res)

            return res

        else:
            raise ValueError("Unsupported syntax elements")


class FinancialCalculator:
    """Financial calculation domain utilities."""

    @staticmethod
    def loan_payment(principal: float, annual_rate: float, years: int) -> dict:
        if principal <= 0 or years <= 0 or annual_rate < 0:
            raise ValueError("Principal, years, and rate must be positive values")

        monthly_rate = (annual_rate / 100) / 12
        total_payments = years * 12

        if monthly_rate == 0:
            monthly_payment = principal / total_payments
        else:
            monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** total_payments) / (((1 + monthly_rate) ** total_payments) - 1)

        total_paid = monthly_payment * total_payments
        total_interest = total_paid - principal

        return {
            "monthly_payment": round(monthly_payment, 2),
            "total_payment": round(total_paid, 2),
            "total_interest": round(total_interest, 2)
        }

    @staticmethod
    def compound_interest(principal: float, annual_rate: float, years: int, frequency: int = 12) -> dict:
        if principal <= 0 or years <= 0 or annual_rate < 0 or frequency <= 0:
            raise ValueError("All parameters must be positive numbers")

        rate_per_period = (annual_rate / 100) / frequency
        total_periods = frequency * years

        future_value = principal * ((1 + rate_per_period) ** total_periods)
        total_interest = future_value - principal

        return {
            "future_value": round(future_value, 2),
            "total_interest": round(total_interest, 2),
            "principal": round(principal, 2)
        }


class UnitConverter:
    """Unit conversion module."""

    CONVERSIONS = {
        "length": {
            "m": 1.0,
            "km": 1000.0,
            "cm": 0.01,
            "mm": 0.001,
            "mile": 1609.344,
            "yard": 0.9144,
            "foot": 0.3048,
            "inch": 0.0254
        },
        "mass": {
            "kg": 1.0,
            "g": 0.001,
            "mg": 0.000001,
            "lb": 0.45359237,
            "oz": 0.028349523125
        },
        "area": {
            "sq_m": 1.0,
            "sq_km": 1000000.0,
            "sq_ft": 0.092903,
            "acre": 4046.86,
            "hectare": 10000.0
        }
    }

    @classmethod
    def convert(cls, category: str, value: float, from_unit: str, to_unit: str) -> float:
        if category == "temperature":
            return cls._convert_temperature(value, from_unit, to_unit)

        if category not in cls.CONVERSIONS:
            raise ValueError(f"Unsupported unit category: {category}")

        units = cls.CONVERSIONS[category]
        if from_unit not in units or to_unit not in units:
            raise ValueError(f"Invalid unit conversion from {from_unit} to {to_unit}")

        base_val = value * units[from_unit]
        target_val = base_val / units[to_unit]
        return round(target_val, 6)

    @staticmethod
    def _convert_temperature(val: float, from_u: str, to_u: str) -> float:
        if from_u == to_u:
            return val
        
        # Convert to Celsius first
        if from_u == "C":
            cels = val
        elif from_u == "F":
            cels = (val - 32) * 5 / 9
        elif from_u == "K":
            cels = val - 273.15
        else:
            raise ValueError("Invalid temperature unit")

        # Convert Celsius to Target
        if to_u == "C":
            return round(cels, 4)
        elif to_u == "F":
            return round((cels * 9 / 5) + 32, 4)
        elif to_u == "K":
            return round(cels + 273.15, 4)
        else:
            raise ValueError("Invalid target temperature unit")