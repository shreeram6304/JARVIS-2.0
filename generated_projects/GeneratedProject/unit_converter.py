from typing import Dict, Any, List

class UnitConverter:
    UNITS: Dict[str, Dict[str, Any]] = {
        "length": {
            "title": "Length",
            "base": "meter",
            "rates": {
                "nanometer": 1e-9,
                "micrometer": 1e-6,
                "millimeter": 0.001,
                "centimeter": 0.01,
                "meter": 1.0,
                "kilometer": 1000.0,
                "inch": 0.0254,
                "foot": 0.3048,
                "yard": 0.9144,
                "mile": 1609.344,
                "nautical_mile": 1852.0
            }
        },
        "weight": {
            "title": "Weight & Mass",
            "base": "kilogram",
            "rates": {
                "milligram": 1e-6,
                "gram": 0.001,
                "kilogram": 1.0,
                "metric_ton": 1000.0,
                "ounce": 0.028349523125,
                "pound": 0.45359237,
                "stone": 6.35029318,
                "short_ton": 907.18474
            }
        },
        "temperature": {
            "title": "Temperature",
            "is_special": True,
            "units": ["celsius", "fahrenheit", "kelvin"]
        },
        "area": {
            "title": "Area",
            "base": "square_meter",
            "rates": {
                "square_millimeter": 1e-6,
                "square_centimeter": 0.0001,
                "square_meter": 1.0,
                "hectare": 10000.0,
                "square_kilometer": 1e6,
                "square_inch": 0.00064516,
                "square_foot": 0.09290304,
                "acre": 4046.8564224,
                "square_mile": 2589988.110336
            }
        },
        "volume": {
            "title": "Volume",
            "base": "liter",
            "rates": {
                "milliliter": 0.001,
                "liter": 1.0,
                "cubic_meter": 1000.0,
                "teaspoon_us": 0.00492892,
                "tablespoon_us": 0.0147868,
                "fluid_ounce_us": 0.0295735,
                "cup_us": 0.236588,
                "pint_us": 0.473176,
                "quart_us": 0.946353,
                "gallon_us": 3.78541
            }
        },
        "speed": {
            "title": "Speed",
            "base": "meters_per_second",
            "rates": {
                "meters_per_second": 1.0,
                "kilometers_per_hour": 1 / 3.6,
                "miles_per_hour": 0.44704,
                "knot": 0.514444,
                "feet_per_second": 0.3048
            }
        }
    }

    @classmethod
    def get_categories(cls) -> Dict[str, Any]:
        result = {}
        for cat_key, cat_data in cls.UNITS.items():
            if cat_data.get("is_special"):
                units = cat_data["units"]
            else:
                units = list(cat_data["rates"].keys())
            result[cat_key] = {
                "title": cat_data["title"],
                "units": units
            }
        return result

    @classmethod
    def convert(cls, category: str, value: float, from_unit: str, to_unit: str) -> float:
        if category not in cls.UNITS:
            raise ValueError(f"Invalid category: {category}")

        cat_data = cls.UNITS[category]

        if category == "temperature":
            return cls._convert_temperature(value, from_unit, to_unit)

        rates = cat_data["rates"]
        if from_unit not in rates:
            raise ValueError(f"Invalid source unit '{from_unit}' for category '{category}'.")
        if to_unit not in rates:
            raise ValueError(f"Invalid destination unit '{to_unit}' for category '{category}'.")

        base_val = value * rates[from_unit]
        converted_val = base_val / rates[to_unit]
        
        if abs(converted_val) < 1e-12:
            return 0.0
        return round(converted_val, 8)

    @classmethod
    def _convert_temperature(cls, value: float, from_unit: str, to_unit: str) -> float:
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()

        if from_unit == to_unit:
            return value

        # Convert source to Celsius
        if from_unit == "celsius":
            celsius = value
        elif from_unit == "fahrenheit":
            celsius = (value - 32) * 5 / 9
        elif from_unit == "kelvin":
            celsius = value - 273.15
        else:
            raise ValueError(f"Unknown temperature unit: {from_unit}")

        # Convert Celsius to destination
        if to_unit == "celsius":
            result = celsius
        elif to_unit == "fahrenheit":
            result = (celsius * 9 / 5) + 32
        elif to_unit == "kelvin":
            result = celsius + 273.15
        else:
            raise ValueError(f"Unknown temperature unit: {to_unit}")

        return round(result, 6)