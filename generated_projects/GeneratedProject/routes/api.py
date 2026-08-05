from flask import Blueprint, request, jsonify
from calculator import SafeMathEngine, FinancialEngine, UnitConverterEngine, HistoryManager

api_bp = Blueprint('api', __name__, url_prefix='/api')
history_store = HistoryManager()

@api_bp.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json() or {}
    expression = data.get('expression', '')

    if not expression:
        return jsonify({'error': 'Expression is required'}), 400

    try:
        raw_result = SafeMathEngine.evaluate(expression)
        
        # Formatting result: int if standard integer, float clean format otherwise
        if raw_result.is_integer():
            formatted_result = str(int(raw_result))
        else:
            formatted_result = f"{raw_result:.8f}".rstrip('0').rstrip('.')

        history_store.add_entry(expression, formatted_result)
        return jsonify({
            'success': True,
            'expression': expression,
            'result': formatted_result
        })
    except ValueError as val_err:
        return jsonify({'success': False, 'error': str(val_err)}), 400
    except Exception as err:
        return jsonify({'success': False, 'error': 'Calculation failed'}), 500


@api_bp.route('/financial', methods=['POST'])
def financial_calc():
    data = request.get_json() or {}
    calc_type = data.get('type')

    try:
        if calc_type == 'loan':
            principal = float(data.get('principal', 0))
            rate = float(data.get('rate', 0))
            years = int(data.get('years', 0))
            res = FinancialEngine.calculate_loan(principal, rate, years)
            return jsonify({'success': True, 'data': res})

        elif calc_type == 'interest':
            principal = float(data.get('principal', 0))
            rate = float(data.get('rate', 0))
            years = float(data.get('years', 0))
            freq = int(data.get('frequency', 12))
            res = FinancialEngine.calculate_compound_interest(principal, rate, years, freq)
            return jsonify({'success': True, 'data': res})

        elif calc_type == 'bmi':
            weight = float(data.get('weight', 0))
            height = float(data.get('height', 0))
            res = FinancialEngine.calculate_bmi(weight, height)
            return jsonify({'success': True, 'data': res})

        else:
            return jsonify({'success': False, 'error': 'Invalid calculation type'}), 400

    except ValueError as ex:
        return jsonify({'success': False, 'error': str(ex)}), 400


@api_bp.route('/convert', methods=['POST'])
def convert_units():
    data = request.get_json() or {}
    category = data.get('category')
    from_unit = data.get('from_unit')
    to_unit = data.get('to_unit')

    try:
        value = float(data.get('value', 0))
        res = UnitConverterEngine.convert(category, from_unit, to_unit, value)
        return jsonify({'success': True, 'result': res})
    except ValueError as ex:
        return jsonify({'success': False, 'error': str(ex)}), 400


@api_bp.route('/history', methods=['GET', 'DELETE'])
def history_api():
    if request.method == 'DELETE':
        history_store.clear()
        return jsonify({'success': True, 'message': 'History cleared'})
    
    return jsonify({'success': True, 'history': history_store.get_history()})