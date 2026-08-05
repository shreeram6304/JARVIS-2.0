class UnitConverterEngine:
    
    # Base conversions factors relative to standard base unit
    CONVERSIONS = {
        'length': {
            'm': 1.0,
            'km': 1000.0,
            'cm': 0.01,
            'mm': 0.001,
            'mi': 1609.344,
            'yd': 0.9144,
            'ft': 0.3048,
            'in': 0.0254
        },
        'mass': {
            'kg': 1.0,
            'g': 0.001,
            'mg': 0.000001,
            'lb': 0.45359237,
            'oz': 0.028349523125
        },
        'volume': {
            'l': 1.0,
            'ml': 0.001,
            'gal': 3.78541,
            'qt': 0.946353,
            'cup': 0.24,
            'fl_oz': 0.0295735
        }
    }

    @classmethod
    def convert(cls, category: str, from_unit: str, to_unit: str, value: float) -> float:
        if category == 'temperature':
            return cls._convert_temperature(from_unit, to_unit, value)

        if category not in cls.CONVERSIONS:
            raise ValueError(f"Unknown unit conversion category: {category}")

        cat_map = cls.CONVERSIONS[category]
        if from_unit not in cat_map or to_unit not in cat_map:
            raise ValueError("Unsupported unit specified")

        # Convert value to base unit, then convert base unit to target unit
        base_value = value * cat_map[from_unit]
        target_value = base_value / cat_map[to_unit]
        return round(target_value, 6)

    @staticmethod
    def _convert_temperature(from_u: str, to_u: str, val: float) -> float:
        from_u = from_u.upper()
        to_u = to_u.upper()

        if from_u == to_u:
            return val

        # Convert from origin to Celsius first
        if from_u == 'C':
            cels = val
        elif from_u == 'F':
            cels = (val - 32) * 5 / 9
        elif from_u == 'K':
            cels = val - 273.15
        else:
            raise ValueError("Unsupported temperature unit")

        # Convert Celsius to destination
        if to_u == 'C':
            res = cels
        elif to_u == 'F':
            res = (cels * 9 / 5) + 32
        elif to_u == 'K':
            res = cels + 273.15
        else:
            raise ValueError("Unsupported temperature unit")

        return round(res, 4)