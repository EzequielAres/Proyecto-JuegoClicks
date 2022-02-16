import pytest
from app import create_app
from werkzeug.datastructures import Headers

@pytest.fixture
def client():
    app = create_app('config_tests.py')

    with app.test_client() as client:
        yield client

def test_getLocations(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/location', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert len(rsp) == 8
    assert "San Fernando" in [d.get("name") for d in rsp]

def test_getLocation(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get("/api/location/1", headers=headers, follow_redirects=True)
    rsp = rv.get_json()

    assert "Cádiz" == rsp.get("name")
    assert [1, 2] == rsp.get("Player")
    assert 1 == rsp.get("region")

def test_postLocation(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.post("/api/location/", headers=headers, follow_redirects=True, json={'name': 'PruebaTest', "region": 1})
    rsp = rv.get_json()

    assert 1 == rsp.get("region")
    assert [] == rsp.get("Player")
    assert "PruebaTest" == rsp.get("name")
    assert 9 == rsp.get("id")

def test_putLocation(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.put("/api/location/1", headers=headers, follow_redirects=True, json={'id': 1, 'name': 'PruebaTest'})
    rsp = rv.get_json()

    assert 1 == rsp.get("region")
    assert [1, 2] == rsp.get("Player")
    assert "PruebaTest" == rsp.get("name")
    assert 1 == rsp.get("id")

def test_delLocation(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.delete("/api/location/1", headers=headers, follow_redirects=True)
    respuesta = rv.status
    assert '204 NO CONTENT' == respuesta

def test_getLocationPoints(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get("/api/location/points/1", headers=headers, follow_redirects=True)
    rsp = rv.get_json()

    assert {"Cádiz" : 0} == rsp;

def test_getLocationsPoints(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get("/api/location/points/", headers=headers, follow_redirects=True)
    rsp = rv.get_json()

    assert "Alcorcón" in [d for d in rsp];
