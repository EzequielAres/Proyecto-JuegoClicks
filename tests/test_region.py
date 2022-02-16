import pytest
from app import create_app
from werkzeug.datastructures import Headers

@pytest.fixture
def client():
    app = create_app('config_tests.py')

    with app.test_client() as client:
        yield client

def test_getRegions(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/region', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert len(rsp) == 6
    assert "Andalucía" in [d.get("name") for d in rsp]

def test_getRegion(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get("/api/region/1", headers=headers, follow_redirects=True)
    rsp = rv.get_json()

    assert [1, 2, 3] == rsp.get("Location")
    assert 1 == rsp.get("country")
    assert "Andalucía" == rsp.get("name")

def test_postRegion(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.post("/api/region/", headers=headers, follow_redirects=True, json={'name': 'PruebaTest', "country": 3})
    rsp = rv.get_json()

    assert [] == rsp.get("Location")
    assert 3 == rsp.get("country")
    assert "PruebaTest" == rsp.get("name")

def test_putRegion(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.put("/api/region/1", headers=headers, follow_redirects=True, json={'id': 1, 'name': 'PruebaTest'})
    rsp = rv.get_json()

    assert [1, 2, 3] == rsp.get("Location")
    assert 1 == rsp.get("country")
    assert "PruebaTest" == rsp.get("name")

def test_delRegion(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.delete("/api/region/1", headers=headers, follow_redirects=True)
    respuesta = rv.status
    assert '204 NO CONTENT' == respuesta

def test_getRegionPoints(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get("/api/region/points/1", headers=headers, follow_redirects=True)
    rsp = rv.get_json()

    assert {"Andalucía" : 0} == rsp;

def test_getRegionsPoints(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get("/api/region/points/", headers=headers, follow_redirects=True)
    rsp = rv.get_json()

    assert "Madrid" in [d for d in rsp];
