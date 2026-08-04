from typing import Dict, Any

CONVERSION_FACTORS = {
    "length": {
        "meter": 1.0,
        "kilometer": 0.001,
        "centimeter": 100.0,
        "millimeter": 1000.0,
        "mile": 0.000621371,
        "yard": 1.09361,
        "foot": 3.28084,
        "inch": 39.3701
    },
    "mass": {
        "kilogram": 1.0,
        "gram": 1000.0,
        "milligram": 1e6,
        "pound": 2.20462,
        "ounce": 35.274,
        "metric_ton": 0.001
    },
    "area": {
        "square_meter": 1.0,
        "square_kilometer": 1e-6,
        "square_foot": 10.7639,
        "square_mile": 3.861e-7,
        "acre": 0.000247105,
        "hectare": 0.0001
    },
    "volume": {
        "liter": 1.0,
        "milliliter": 1000.0,
        "cubic_meter": 0.001,
        "gallon": 0.264172,
        "quart": 1.05669,
        "pint": 2.11338,
        "cup": 4.16667
    },
    "digital": {
        "byte": 1.0,
        "kilobyte": 1e-3,
        "megabyte": 1e-6,
        "gigabyte": 1e-9,
        "terabyte": 1e-12,
        "bit": 8.0
    }
}

def convert_units(category: str, from_unit: str, to_unit: str, value: float) -> Dict[str, Any]:
    category = category.lower()
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    if category == "temperature":
        return convert_temperature(from_unit, to_unit, value)

    if category not in CONVERSION_FACTORS:
        raise ValueError(f"Unknown conversion category: '{category}'")

    cat_units = CONVERSION_FACTORS[category]
    if from_unit not in cat_units:
        raise ValueError(f"Invalid source unit '{from_unit}' for category '{category}'")
    if to_unit not in cat_units:
        raise ValueError(f"Invalid target unit '{to_unit}' for category '{category}'")

    # Base conversion
    base_val = value / cat_units[from_unit]
    converted = base_val * cat_units[to_unit]

    return {
        "category": category,
        "from_unit": from_unit,
        "to_unit": to_unit,
        "from_value": value,
        "result": round(converted, 8)
    }

def convert_temperature(from_unit: str, to_unit: str, val: float) -> Dict[str, Any]:
    # Normalize to Celsius
    if from_unit in ("celsius", "c"):
        c_val = val
    elif from_unit in ("fahrenheit", "f"):
        c_val = (val - 32.0) * (5.0 / 9.0)
    elif from_unit in ("kelvin", "k"):
        c_val = val - 273.15
    else:
        raise ValueError(f"Invalid temperature unit: '{from_unit}'")

    # Convert Celsius to target
    if to_unit in ("celsius", "c"):
        res = c_val
    elif to_unit in ("fahrenheit", "f"):
        res = (c_val * 9.0 / 5.0) + 32.0
    elif to_unit in ("kelvin", "k"):
        res = c_val + 273.15
    else:
        raise ValueError(f"Invalid temperature unit: '{to_unit}'")

    return {
        "category": "temperature",
        "from_unit": from_unit,
        "to_unit": to_unit,
        "from_value": val,
        "result": round(res, 4)
    }