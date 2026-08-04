import pytest
from app import app, safe_evaluate

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_safe_evaluate_basic():
    assert safe_evaluate("2 + 2") == "4"
    assert safe_evaluate("10 - 4 * 2") == "2"
    assert safe_evaluate("(5 + 3) * 2") == "16"
    assert safe_evaluate("10 / 4") == "2.5"

def test_safe_evaluate_scientific():
    assert safe_evaluate("sin(90)", angle_unit="deg") == "1"
    assert safe_evaluate("cos(0)", angle_unit="deg") == "1"
    assert safe_evaluate("sqrt(16)") == "4"
    assert safe_evaluate("2 ^ 3") == "8"

def test_calculate_endpoint(client):
    response = client.post('/api/calculate', json={'expression': '15 + 27', 'angle_unit': 'deg'})
    data = response.get_json()
    assert response.status_code == 200
    assert data['success'] is True
    assert data['result'] == '42'

def test_invalid_expression(client):
    response = client.post('/api/calculate', json={'expression': '2 // 0'})
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False

def test_history_endpoint(client):
    client.post('/api/calculate', json={'expression': '5 * 5', 'angle_unit': 'deg'})
    response = client.get('/api/history')
    data = response.get_json()
    assert response.status_code == 200
    assert len(data['history']) > 0

    del_resp = client.delete('/api/history')
    assert del_resp.status_code == 200
    
    history_after = client.get('/api/history').get_json()
    assert len(history_after['history']) == 0