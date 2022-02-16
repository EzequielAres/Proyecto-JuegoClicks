import io

import pytest
from app import create_app
from werkzeug.datastructures import Headers

@pytest.fixture
def client():
    app = create_app('config_tests.py')

    with app.test_client() as client:
        yield client

def test_getPlayers(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/player', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert len(rsp) == 10
    assert "Ezequiel" in [d.get("username") for d in rsp]

def test_getPlayer(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get("/api/player/1", headers=headers, follow_redirects=True)
    rsp = rv.get_json()

    assert "Ezequiel" == rsp.get("username")
    assert "/static/imagenes/anon.jpg" == rsp.get("imagen")
    assert 1 == rsp.get("location")
    assert 0 == rsp.get("puntos")
    assert 1 == rsp.get("user")
    assert [1,2] == rsp.get("teams")

def test_postPlayer(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.post("/api/player/", headers=headers, follow_redirects=True, json={'username': 'PruebaTest', "user": 3, "puntos": 10, "teams": [1, 2], "location": 2})
    rsp = rv.get_json()

    assert "PruebaTest" == rsp.get("username")
    assert 3 == rsp.get("user")
    assert 10 == rsp.get("puntos")
    assert [1, 2] == rsp.get("teams")
    assert 2 == rsp.get("location")
    assert "/static/imagenes/anon.jpg" == rsp.get("imagen")

def test_putPlayer(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.put("/api/player/1", headers=headers, follow_redirects=True, json={'id': 1, 'username': 'PruebaTest', "puntos": 40, "teams": [1, 2, 3], "location": 3, "imagen" : "/static/imagenes/prueba.jpg"})
    rsp = rv.get_json()

    assert "PruebaTest" == rsp.get("username")
    assert 1 == rsp.get("user")
    assert 40 == rsp.get("puntos")
    assert [1, 2, 3] == rsp.get("teams")
    assert 3 == rsp.get("location")
    assert "/static/imagenes/prueba.jpg" == rsp.get("imagen")

def test_delPlayer(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.delete("/api/player/1", headers=headers, follow_redirects=True)
    respuesta = rv.status
    assert '204 NO CONTENT' == respuesta

def test_postPlayerPoints(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.post("/api/player/points/1", headers=headers, follow_redirects=True, json={'clicks': 10})
    respuesta = rv.status
    assert '201 CREATED' == respuesta

def test_getPlayerPoints(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get("/api/player/points/1", headers=headers, follow_redirects=True)
    rsp = rv.get_json()

    assert 0 == rsp;

def test_getPlayersPoints(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get("/api/player/points/", headers=headers, follow_redirects=True)
    rsp = rv.get_json()

    assert {'id': 1,
  'imagen': '/static/imagenes/anon.jpg',
  'puntos': 0,
  'username': 'Ezequiel'} in [d for d in rsp];


def test_postPlayerImage(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")

    data = {'imagen' : ""}
    data['imagen'] = (io.BytesIO(b"abcdef"), 'test.jpg')
    rv = client.post("/api/player/subir/1", data=data, headers=headers, follow_redirects=True, content_type='multipart/form-data')
    rsp = rv.get_json()

    assert rsp.get("imagen") == "/static/imagenes/test.jpg"

