class UnitConverter:
    """
    Handles unit conversions across multiple dimensions.
    """

    CONVERSIONS = {
        'length': {
            'meter': 1.0,
            'kilometer': 1000.0,
            'centimeter': 0.01,
            'millimeter': 0.001,
            'mile': 1609.344,
            'yard': 0.9144,
            'foot': 0.3048,
            'inch': 0.0254
        },
        'mass': {
            'kilogram': 1.0,
            'gram': 0.001,
            'milligram': 0.000001,
            'pound': 0.45359237,
            'ounce': 0.028349523125,
            'metric_ton': 1000.0
        },
        'area': {
            'square_meter': 1.0,
            'square_kilometer': 1000000.0,
            'square_foot': 0.09290304,
            'square_mile': 2589988.110336,
            'acre': 4046.8564224,
            'hectare': 10000.0
        },
        'volume': {
            'liter': 1.0,
            'milliliter': 0.001,
            'cubic_meter': 1000.0,
            'gallon_us': 3.785411784,
            'quart_us': 0.946352946,
            'pint_us': 0.473176473,
            'cup': 0.24
        },
        'speed': {
            'meters_per_sec': 1.0,
            'km_per_hour': 0.277777778,
            'miles_per_hour': 0.44704,
            'knot': 0.514444444
        }
    }

    @classmethod
    def get_categories(cls):
        categories = {}
        for cat, units in cls.CONVERSIONS.items():
            categories[cat] = list(units.keys())
        categories['temperature'] = ['celsius', 'fahrenheit', 'kelvin']
        return categories

    @classmethod
    def convert(cls, category: str, from_unit: str, to_unit: str, value: float) -> float:
        category = category.lower()
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()

        if category == 'temperature':
            return cls._convert_temperature(from_unit, to_unit, value)

        if category not in cls.CONVERSIONS:
            raise ValueError(f"Unknown conversion category: {category}")

        cat_map = cls.CONVERSIONS[category]
        if from_unit not in cat_map or to_unit not in cat_map:
            raise ValueError(f"Invalid units for {category}: {from_unit} -> {to_unit}")

        base_val = value * cat_map[from_unit]
        target_val = base_val / cat_map[to_unit]
        return target_val

    @staticmethod
    def _convert_temperature(from_unit: str, to_unit: str, val: float) -> float:
        if from_unit == to_unit:
            return val

        # Convert to Celsius first
        if from_unit == 'celsius':
            celsius = val
        elif from_unit == 'fahrenheit':
            celsius = (val - 32) * 5 / 9
        elif from_unit == 'kelvin':
            celsius = val - 273.15
        else:
            raise ValueError(f"Invalid temperature unit: {from_unit}")

        # Convert Celsius to Target
        if to_unit == 'celsius':
            return celsius
        elif to_unit == 'fahrenheit':
            return (celsius * 9 / 5) + 32
        elif to_unit == 'kelvin':
            return celsius + 273.15
        else:
            raise ValueError(f"Invalid temperature unit: {to_unit}")