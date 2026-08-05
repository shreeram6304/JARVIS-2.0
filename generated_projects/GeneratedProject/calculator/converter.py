from typing import Dict, Any

class UnitConverter:
    """
    Handles unit conversions across multiple physical dynamic categories.
    """

    CONVERSIONS: Dict[str, Dict[str, float]] = {
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
        "digital": {
            "B": 1.0,
            "KB": 1024.0,
            "MB": 1048576.0,
            "GB": 1073741824.0,
            "TB": 1099511627776.0
        }
    }

    @classmethod
    def convert(cls, category: str, value: float, from_unit: str, to_unit: str) -> float:
        """
        Converts value from one unit to another within a given category.
        """
        category = category.lower()

        if category == "temperature":
            return cls._convert_temperature(value, from_unit, to_unit)

        if category not in cls.CONVERSIONS:
            raise ValueError(f"Invalid category: {category}")

        units = cls.CONVERSIONS[category]
        if from_unit not in units or to_unit not in units:
            raise ValueError(f"Invalid units for category '{category}': {from_unit} to {to_unit}")

        # Standard conversion via base unit factor
        base_value = value * units[from_unit]
        return base_value / units[to_unit]

    @staticmethod
    def _convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
        from_u = from_unit.upper()
        to_u = to_unit.upper()

        if from_u == to_u:
            return value

        # First convert source unit to Celsius
        if from_u == "C":
            celsius = value
        elif from_u == "F":
            celsius = (value - 32) * 5 / 9
        elif from_u == "K":
            celsius = value - 273.15
        else:
            raise ValueError(f"Invalid temperature unit: {from_unit}")

        # Convert Celsius to destination unit
        if to_u == "C":
            return celsius
        elif to_u == "F":
            return (celsius * 9 / 5) + 32
        elif to_u == "K":
            return celsius + 273.15
        else:
            raise ValueError(f"Invalid temperature unit: {to_unit}")

    @classmethod
    def get_supported_units(cls) -> Dict[str, list]:
        """Returns map of available categories and units."""
        units_map = {cat: list(units.keys()) for cat, units in cls.CONVERSIONS.items()}
        units_map["temperature"] = ["C", "F", "K"]
        return units_map