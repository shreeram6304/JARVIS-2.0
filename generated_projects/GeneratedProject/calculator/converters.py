from typing import Dict, Any

class UnitConverter:
    """Provides standard physical and digital unit conversion calculations."""

    def __init__(self):
        # Conversion base factors to standard base units:
        # Length -> meters (m)
        # Mass -> kilograms (kg)
        # Temperature -> special formulas
        # Area -> square meters (m²)
        # Volume -> liters (L)
        # Speed -> meters per second (m/s)
        # Digital -> bytes (B)
        
        self.units = {
            'length': {
                'm': 1.0,
                'km': 1000.0,
                'cm': 0.01,
                'mm': 0.001,
                'mile': 1609.344,
                'yard': 0.9144,
                'foot': 0.3048,
                'inch': 0.0254
            },
            'mass': {
                'kg': 1.0,
                'g': 0.001,
                'mg': 0.000001,
                'lb': 0.45359237,
                'oz': 0.028349523125,
                'metric_ton': 1000.0
            },
            'area': {
                'sq_m': 1.0,
                'sq_km': 1000000.0,
                'sq_ft': 0.09290304,
                'sq_mile': 2589988.110336,
                'acre': 4046.8564224,
                'hectare': 10000.0
            },
            'volume': {
                'liter': 1.0,
                'milliliter': 0.001,
                'cubic_m': 1000.0,
                'gallon_us': 3.785411784,
                'quart_us': 0.946352946,
                'cup': 0.24,
                'fluid_oz': 0.0295735
            },
            'speed': {
                'm_s': 1.0,
                'km_h': 0.2777777777777778,
                'mph': 0.44704,
                'knot': 0.5144444444444445
            },
            'digital': {
                'B': 1.0,
                'KB': 1024.0,
                'MB': 1048576.0,
                'GB': 1073741824.0,
                'TB': 1099511627776.0
            }
        }

    def get_supported_units(self) -> Dict[str, list]:
        """Return dict of available categories and their supported unit codes."""
        categories = {cat: list(units.keys()) for cat, units in self.units.items()}
        categories['temperature'] = ['celsius', 'fahrenheit', 'kelvin']
        return categories

    def convert(self, category: str, from_unit: str, to_unit: str, value: float) -> Dict[str, Any]:
        """Convert a value from one unit to another."""
        category = category.lower()
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()

        if category == 'temperature':
            return self._convert_temperature(from_unit, to_unit, value)

        if category not in self.units:
            return {'status': 'error', 'message': f"Unsupported unit category: '{category}'"}

        cat_units = self.units[category]
        if from_unit not in cat_units:
            return {'status': 'error', 'message': f"Unknown unit '{from_unit}' in category '{category}'"}
        if to_unit not in cat_units:
            return {'status': 'error', 'message': f"Unknown unit '{to_unit}' in category '{category}'"}

        # Convert value to base unit, then convert base unit to target unit
        base_value = value * cat_units[from_unit]
        target_value = base_value / cat_units[to_unit]

        # Format result nicely
        if target_value.is_integer():
            res = float(int(target_value))
        else:
            res = round(target_value, 8)

        return {
            'status': 'success',
            'category': category,
            'from_unit': from_unit,
            'to_unit': to_unit,
            'value': value,
            'result': res,
            'formatted_result': f"{res:g}"
        }

    def _convert_temperature(self, from_unit: str, to_unit: str, value: float) -> Dict[str, Any]:
        """Special conversion handling for temperature scales."""
        # Convert to Celsius first
        if from_unit == 'celsius' or from_unit == 'c':
            c_val = value
        elif from_unit == 'fahrenheit' or from_unit == 'f':
            c_val = (value - 32.0) * (5.0 / 9.0)
        elif from_unit == 'kelvin' or from_unit == 'k':
            c_val = value - 273.15
        else:
            return {'status': 'error', 'message': f"Unknown temperature unit '{from_unit}'"}

        # Convert Celsius to target unit
        if to_unit == 'celsius' or to_unit == 'c':
            target_val = c_val
        elif to_unit == 'fahrenheit' or to_unit == 'f':
            target_val = (c_val * 9.0 / 5.0) + 32.0
        elif to_unit == 'kelvin' or to_unit == 'k':
            target_val = c_val + 273.15
        else:
            return {'status': 'error', 'message': f"Unknown temperature unit '{to_unit}'"}

        res = round(target_val, 6)
        return {
            'status': 'success',
            'category': 'temperature',
            'from_unit': from_unit,
            'to_unit': to_unit,
            'value': value,
            'result': res,
            'formatted_result': f"{res:g}"
        }