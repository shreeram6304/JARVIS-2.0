import os
import sqlite3
from flask import Flask, render_template, request, jsonify
from calculator.engine import MathEngine
from calculator.converters import UnitConverter
from calculator.history import HistoryManager

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'jarvis-calculator-secret-key-2025')

# Initialize core modules
engine = MathEngine()
converter = UnitConverter()
history_db = os.path.join(app.instance_path, 'calculator_history.db')

# Ensure instance folder exists
os.makedirs(app.instance_path, exist_ok=True)

history_mgr = HistoryManager(db_path=history_db)

@app.route('/')
def index():
    """Render the main calculator interface."""
    return render_template('index.html')

@app.route('/api/calculate', methods=['POST'])
def calculate():
    """API endpoint to evaluate mathematical expressions."""
    data = request.get_json() or {}
    expression = data.get('expression', '')
    angle_mode = data.get('angle_mode', 'DEG')

    if not expression or not isinstance(expression, str):
        return jsonify({'status': 'error', 'message': 'Expression is required'}), 400

    if angle_mode not in ('DEG', 'RAD'):
        angle_mode = 'DEG'

    result_data = engine.evaluate(expression, angle_mode=angle_mode)

    if result_data['status'] == 'success':
        # Save to history
        history_mgr.add_entry(
            expression=expression,
            result=result_data['result'],
            calc_type='scientific' if result_data.get('is_scientific') else 'standard'
        )
        return jsonify({
            'status': 'success',
            'expression': expression,
            'result': result_data['result'],
            'formatted_result': result_data['formatted_result']
        })
    else:
        return jsonify({
            'status': 'error',
            'message': result_data['message']
        }), 400

@app.route('/api/convert', methods=['POST'])
def convert():
    """API endpoint for unit conversion."""
    data = request.get_json() or {}
    category = data.get('category', '')
    from_unit = data.get('from_unit', '')
    to_unit = data.get('to_unit', '')
    try:
        value = float(data.get('value', 0))
    except (ValueError, TypeError):
        return jsonify({'status': 'error', 'message': 'Invalid numeric value'}), 400

    result = converter.convert(category, from_unit, to_unit, value)
    
    if result['status'] == 'success':
        # Record conversion in history
        expr_str = f"{value} {from_unit} to {to_unit}"
        res_str = f"{result['result']} {to_unit}"
        history_mgr.add_entry(expression=expr_str, result=res_str, calc_type='converter')
        return jsonify(result)
    else:
        return jsonify(result), 400

@app.route('/api/converter/units', methods=['GET'])
def get_converter_units():
    """Retrieve available unit conversion categories and units."""
    return jsonify({
        'status': 'success',
        'categories': converter.get_supported_units()
    })

@app.route('/api/history', methods=['GET'])
def get_history():
    """Fetch recent calculation history."""
    limit = request.args.get('limit', default=30, type=int)
    history = history_mgr.get_history(limit=limit)
    return jsonify({
        'status': 'success',
        'history': history
    })

@app.route('/api/history', methods=['DELETE'])
def clear_history():
    """Clear calculation history."""
    history_mgr.clear_history()
    return jsonify({
        'status': 'success',
        'message': 'History cleared successfully'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)