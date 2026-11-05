import pytest
from app import app
from models import User
from peewee import SqliteDatabase
from services import create_user


@pytest.fixture()
def test_app():
    new_app = app
    new_app.config.update({'TESTING': True})

    yield new_app

@pytest.fixture()
def client(test_app):
    return test_app.test_client()


def test_json_data(client, test_database):
    response = client.put(f'/users/{test_database.id}', json={
        'age': 20
    })
    assert response.status_code == 200
    assert response.json['age'] == 20

def test_404(client, test_database):
    response = client.put(f'/users/{test_database.id + 1000}', json={
        'age': 50
    })

    assert response.status_code == 404
    assert response.json['error'] == 'Not Found'

def test_incorrect_age(client, test_database):
    response = client.put(f'/users/{test_database.id}', json={
        'age': -1
    })

    assert response.status_code == 400
    assert response.json['error'] == 'Bad Request'

def test_incorrect_type_of_data(client, test_database):
    response = client.put(f'/users/{test_database.id}', json=[
        'ivan', 25])

    assert response.status_code == 400
    assert response.json['error'] == 'Bad Request'
    assert type(response.json) == dict

def test_empty_json(client, test_database):

    response = client.put(f'/users/{test_database.id}', json={})

    assert response.status_code == 400
    assert response.json['error'] == 'Bad Request'

def test_incorrect_field(client, test_database):

    response = client.put(f'/users/{test_database.id}', json={
        'email': 'ivanov1984@mail.ru',
    })

    assert response.status_code == 400
    assert response.json['error'] == 'Bad Request'

def test_incorrect_type_of_value(client, test_database):
    response = client.put(f'/users/{test_database.id}', json={
        'age': '25'
    })

    assert response.status_code == 400
    assert response.json['error'] == 'Bad Request'

def test_not_empty_string_name(client, test_database):
    response = client.put(f'/users/{test_database.id}', json={
        'name': '     '
    })

    assert response.status_code == 400
    assert response.json['error'] == 'Bad Request'

def test_not_empty_string_surname(client, test_database):
    response = client.put(f'/users/{test_database.id}', json={
        'surname': '     '
    })

    assert response.status_code == 400
    assert response.json['error'] == 'Bad Request'


def test_age_zero_rejected(client, test_database):
    response = client.put(f'/users/{test_database.id}', json={
        'age': 0
    })

    assert response.status_code == 400
    assert response.json['error'] == 'Bad Request'

def test_particular_update(client, test_database):

    name = test_database.name
    surname = test_database.surname
    age_before_update = test_database.age

    response = client.put(f'/users/{test_database.id}', json={
        'age': 98
    })

    assert response.status_code == 200
    assert response.json['age'] != age_before_update
    assert response.json['age'] == 98
    assert response.json['surname'] == surname and response.json['name'] == name

def test_errors_absence_if_mistake(client, test_database):

    users_before_update = User.select().count()

    response = client.put(f'/users/{test_database.id + 1000}', json={
        'age': 20
    })

    users_after_update = User.select().count()

    assert response.status_code == 404
    assert response.json['error'] == 'Not Found'
    assert users_before_update == users_after_update

def test_delete_user(client, test_database):

    id_before_delete = test_database.id

    response = client.delete(f'/users/{test_database.id}')

    assert response.status_code == 200
    assert User.select().where(User.id == id_before_delete).count() == 0

def test_delete_user(client, test_database):

    total = User.select().count()

    response = client.delete(f'/users/{test_database.id + 1000}')

    assert response.status_code == 404
    assert response.json['error'] == 'Not Found'
    assert User.select().count() == total


def test_get_users(client, test_database):
    response = client.get('/users')

    assert response.status_code == 200

    users = response.json

    assert len(users) == 1
    assert users[0]['id'] == test_database.id
    assert users[0]['name'] == test_database.name
    assert users[0]['surname'] == test_database.surname
    assert users[0]['age'] == test_database.age



db_for_tests = SqliteDatabase(':memory:')


MODELS = [User]

@pytest.fixture()
def test_database():
    with db_for_tests.bind_ctx(MODELS):
        try:
            db_for_tests.connect()
            db_for_tests.create_tables(MODELS)

            user = create_user('ivan', 'ivanov', 24)

            yield user


        finally:
            db_for_tests.drop_tables(MODELS)
            db_for_tests.close()
