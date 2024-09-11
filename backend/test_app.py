# Unitariy tests
import pytest
from app import app, db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

        with app.app_context():
            db.session.remove()
            db.drop_all()


def login(client):
    response = client.post('/login', json={
        'username': 'test_user',
        'password': 'test_pass'

    })
    token = response.get_json()['access_token']
    return token


def test_create_owner(client):
    token = login(client)
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = client.post(
        '/owner', json={'name': 'John Doe'}, headers=headers)
    assert response.status_code == 201


def test_add_vehicle(client):
    token = login(client)
    headers = {
        'Authorization': f'Bearer {token}'
    }
    client.post('/owner', json={'name': 'John Doe'}, headers=headers)
    response = client.post(
        '/owner/1/vehicle', json={'color': 'yellow', 'model': 'hatch'},
        headers=headers)
    assert response.status_code == 201


def test_list_owners(client):
    token = login(client)
    headers = {
        'Authorization': f'Bearer {token}'
    }
    client.post('/owner', json={'name': 'John Doe'}, headers=headers)
    client.post('/owner/1/vehicle',
                json={'color': 'yellow', 'model': 'hatch'}, headers=headers)
    response = client.get('/owners', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['name'] == 'John Doe'
    assert len(data[0]['vehicles']) == 1
    assert data[0]['vehicles'][0]['color'] == 'yellow'
    assert data[0]['vehicles'][0]['model'] == 'hatch'
