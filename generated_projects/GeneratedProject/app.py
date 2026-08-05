from flask import Flask, render_template, request, jsonify
from calculator import MathEvaluator, UnitConverter, HistoryManager

app = Flask(__name__)
history_store = HistoryManager(max_items=50)

@app.route("/")
def index():
    """Renders the single page application calculator UI."""
    return render_template("index.html")

@app.route("/api/calculate", methods=["POST"])
def calculate():
    """Endpoint for evaluating mathematical expressions."""
    data = request.get_json() or {}
    expression = data.get("expression", "")

    if not expression:
        return jsonify({"success": False, "error": "No expression provided."}), 400

    try:
        result = MathEvaluator.evaluate(expression)
        
        # Format floating numbers nicely
        if isinstance(result, float):
            result = round(result, 10)
            if result.is_integer():
                result = int(result)

        entry = history_store.add_entry(expression, result)
        return jsonify({
            "success": True,
            "expression": expression,
            "result": result,
            "history_item": entry
        })
    except (ValueError, ZeroDivisionError) as err:
        return jsonify({"success": False, "error": str(err)}), 400
    except Exception:
        return jsonify({"success": False, "error": "An unexpected error occurred."}), 500

@app.route("/api/convert", methods=["POST"])
def convert():
    """Endpoint for converting physical units."""
    data = request.get_json() or {}
    category = data.get("category", "")
    value = data.get("value", 0)
    from_unit = data.get("from_unit", "")
    to_unit = data.get("to_unit", "")

    try:
        num_value = float(value)
        converted_value = UnitConverter.convert(category, num_value, from_unit, to_unit)
        rounded_result = round(converted_value, 8)
        if rounded_result.is_integer():
            rounded_result = int(rounded_result)

        return jsonify({
            "success": True,
            "result": rounded_result,
            "category": category,
            "from_unit": from_unit,
            "to_unit": to_unit
        })
    except ValueError as err:
        return jsonify({"success": False, "error": str(err)}), 400
    except Exception:
        return jsonify({"success": False, "error": "Unit conversion failed."}), 500

@app.route("/api/units", methods=["GET"])
def get_units():
    """Endpoint returning available conversion units."""
    return jsonify({"success": True, "units": UnitConverter.get_supported_units()})

@app.route("/api/history", methods=["GET", "DELETE"])
def handle_history():
    """Endpoint for retrieving or clearing history."""
    if request.method == "DELETE":
        history_store.clear()
        return jsonify({"success": True, "message": "History cleared."})
    
    return jsonify({"success": True, "history": history_store.get_all()})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)