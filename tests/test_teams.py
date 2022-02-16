import io

import pytest
from app import create_app
from werkzeug.datastructures import Headers

@pytest.fixture
def client():
    app = create_app('config_tests.py')

    with app.test_client() as client:
        yield client

def test_getTeams(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/team', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert len(rsp) == 5
    assert "Equipo1" in [d.get("name") for d in rsp]

def test_getTeam(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get("/api/team/1", headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert "Equipo1" == rsp.get("name")
    assert 1 == rsp.get("id")
    assert "/static/imagenes/anon.jpg" == rsp.get("imagen")

def test_postTeam(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.post("/api/team/", headers=headers, follow_redirects=True, json={'name': 'Equipo6', 'imagen': '/static/imagenes/anon.jpg'})
    rsp = rv.get_json()
    assert "Equipo6" == rsp.get("name")
    assert '/static/imagenes/anon.jpg' == rsp.get("imagen")

def test_putTeam(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.put("/api/team/1", headers=headers, follow_redirects=True, json={'id': 1, 'name': 'EquipoCambio', 'imagen': '/static/imagenes/cambio.jpg'})
    rsp = rv.get_json()

    assert "EquipoCambio" == rsp.get('name')
    assert 1 == rsp.get("id")
    assert '/static/imagenes/cambio.jpg' == rsp.get("imagen")

def test_delTeam(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.delete("/api/team/1", headers=headers, follow_redirects=True)
    respuesta = rv.status
    assert '204 NO CONTENT' == respuesta

def test_getPointsTeam(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get("/api/team/points/1", headers=headers, follow_redirects=True)
    respuesta = rv.get_json()

    assert {'Equipo1' : 0} == respuesta

def test_getPointsTeams(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get("/api/team/points/", headers=headers, follow_redirects=True)
    respuesta = rv.get_json()
    assert 'Equipo1' in [d for d in respuesta]

def test_postTeamImage(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")

    data = {'imagen' : ""}
    data['imagen'] = (io.BytesIO(b"abcdef"), 'test.jpg')
    rv = client.post("/api/team/subir/1", data=data, headers=headers, follow_redirects=True, content_type='multipart/form-data')
    rsp = rv.get_json()

    assert rsp.get("imagen") == "/static/imagenes/test.jpg"