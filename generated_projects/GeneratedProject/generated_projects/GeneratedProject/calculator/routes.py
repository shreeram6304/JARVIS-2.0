from flask import Blueprint, request, jsonify
from calculator.engine import SafeMathEvaluator, MathEngineError
from calculator.history import HistoryManager

api_bp = Blueprint("api", __name__, url_prefix="/api")
evaluator = SafeMathEvaluator()
history_mgr = HistoryManager()

@api_bp.route("/calculate", methods=["POST"])
def calculate():
    """Endpoint to evaluate a mathematical expression."""
    data = request.get_json() or {}
    expression = data.get("expression", "")

    if not expression:
        return jsonify({"success": False, "error": "No expression provided"}), 400

    try:
        result = evaluator.evaluate(expression)
        entry = history_mgr.add_entry(expression, str(result))
        return jsonify({
            "success": True,
            "expression": expression,
            "result": result,
            "history_item": entry
        }), 200
    except MathEngineError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"An unexpected error occurred: {str(e)}"}), 500

@api_bp.route("/history", methods=["GET"])
def get_history():
    """Endpoint to fetch calculation history."""
    try:
        recent = history_mgr.get_recent(limit=50)
        return jsonify({"success": True, "history": recent}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@api_bp.route("/history", methods=["DELETE"])
def clear_history():
    """Endpoint to clear calculation history."""
    try:
        history_mgr.clear()
        return jsonify({"success": True, "message": "History cleared successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500