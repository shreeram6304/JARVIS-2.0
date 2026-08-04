import pytest
import math
from app import app
from calculator_engine import SafeCalculatorEngine, UnitConverter, CalculationError

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# --- SafeCalculatorEngine Tests ---

def test_basic_arithmetic():
    engine = SafeCalculatorEngine()
    assert engine.evaluate("2 + 2") == 4
    assert engine.evaluate("10 - 4 * 2") == 2
    assert engine.evaluate("(10 - 4) * 2") == 12
    assert engine.evaluate("15 / 3") == 5

def test_scientific_functions():
    engine = SafeCalculatorEngine()
    assert engine.evaluate("sin(0)") == 0
    assert engine.evaluate("cos(0)") == 1
    assert engine.evaluate("sqrt(16)") == 4
    assert engine.evaluate("factorial(5)") == 120
    assert math.isclose(engine.evaluate("pi"), math.pi)

def test_syntax_errors():
    engine = SafeCalculatorEngine()
    with pytest.raises(CalculationError, match="Invalid mathematical expression syntax"):
        engine.evaluate("2 + +")

def test_zero_division():
    engine = SafeCalculatorEngine()
    with pytest.raises(CalculationError, match="Division by zero is undefined"):
        engine.evaluate("10 / 0")

def test_security_eval_blocking():
    engine = SafeCalculatorEngine()
    # Ensure arbitrary code execution is prevented safely
    with pytest.raises(CalculationError):
        engine.evaluate("__import__('os').system('echo hack')")

# --- Unit Converter Tests ---

def test_length_conversion():
    res = UnitConverter.convert('length', 'km', 'm', 5)
    assert res == 5000.0

def test_temperature_conversion():
    res = UnitConverter.convert('temperature', 'c', 'f', 0)
    assert res == 32.0
    res2 = UnitConverter.convert('temperature', 'f', 'c', 212)
    assert res2 == 100.0

# --- API Endpoints Integration Tests ---

def test_api_calculate_success(client):
    rv = client.post('/api/calculate', json={'expression': '25 * 4'})
    data = rv.get_json()
    assert rv.status_code == 200
    assert data['status'] == 'success'
    assert data['formatted_result'] == '100'

def test_api_calculate_error(client):
    rv = client.post('/api/calculate', json={'expression': '10 / 0'})
    data = rv.get_json()
    assert rv.status_code == 400
    assert data['status'] == 'error'
    assert 'zero' in data['message'].lower()

def test_api_convert_success(client):
    rv = client.post('/api/convert', json={
        'category': 'length',
        'from_unit': 'm',
        'to_unit': 'cm',
        'value': 2.5
    })
    data = rv.get_json()
    assert rv.status_code == 200
    assert data['status'] == 'success'
    assert data['formatted_result'] == '250'

def test_api_history_flow(client):
    # Clear history first
    client.post('/api/history/clear')
    
    # Post calculation
    client.post('/api/calculate', json={'expression': '5 + 5'})
    
    # Query history
    rv = client.get('/api/history')
    data = rv.get_json()
    assert rv.status_code == 200
    assert len(data['history']) == 1
    assert data['history'][0]['expression'] == '5 + 5'
    assert data['history'][0]['result'] == '10'