import pytest
from app import create_app
from werkzeug.datastructures import Headers

@pytest.fixture
def client():
    app = create_app('config_tests.py')

    with app.test_client() as client:
        yield client


def test_prueba(client):
    rv = client.get('/')
    assert "Here is the" in rv.get_data(as_text=True)

def test_login(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()


def test_getUsers(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/user', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert len(rsp) == 10
    assert "Ezequiel" in [d.get("username") for d in rsp]

def test_getUser(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get("/api/user/1", headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert "Ezequiel" == rsp.get("username")
    assert 1 == rsp.get("id")
    assert "ezequiel@ejemplo.com" == rsp.get("email")
    assert True == rsp.get("is_active")
    assert 1 == rsp.get("player")
    assert [1] == rsp.get("roles")

def test_postUser(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.post("/api/user/", headers=headers, follow_redirects=True, json={'username': 'Antoñete', 'email': 'antoñete@ejemplo.com', 'hashed_password': 'pestillo'})
    rsp = rv.get_json()

    assert "Antoñete" == rsp.get("username")
    assert 11 == rsp.get("id")
    assert "antoñete@ejemplo.com" == rsp.get("email")
    assert True == rsp.get("is_active")
    assert None == rsp.get("player")
    assert [] == rsp.get("roles")


def test_putUser(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.put("/api/user/1", headers=headers, follow_redirects=True, json={'id': 1, 'email': 'ezequielCambio@ejemplo.com', 'username': 'EzequielCambio'})
    rsp = rv.get_json()

    assert "EzequielCambio" == rsp.get("username")
    assert 1 == rsp.get("id")
    assert "ezequielCambio@ejemplo.com" == rsp.get("email")
    assert True == rsp.get("is_active")
    assert 1 == rsp.get("player")
    assert [1] == rsp.get("roles")

def test_delUser(client):
    rv = client.post('/login', json={'username': 'Ezequiel', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.delete("/api/user/1", headers=headers, follow_redirects=True)
    respuesta = rv.status
    assert '204 NO CONTENT' == respuesta
