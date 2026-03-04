from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_root_deve_retornar_ola_mundo(client):
    """
    Esse teste tem 3 etapas (AAA)
    1. Arrange: Preparar o cenário do teste
    2. Act: Executar a ação que queremos testar
    3. Assert: Verificar se o resultado é o esperado
    """
    # client = TestClient(app) DRY - Don't Repeat Yourself

    response = client.get('/')

    assert response.json() == {'message': 'Olá Mundo!'}
    assert response.status_code == HTTPStatus.OK


def test_root_deve_retornar_ola_mundo_html(client):
    # client = TestClient(app) DRY

    response = client.get('/html')

    assert response.status_code == HTTPStatus.OK
    assert '<h1>Olá, Mundo!</h1>' in response.text


def test_create_user(client):
    # client = TestClient(app) DRY

    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_username_already_created(client, user):
    # user_schema = UserSchema.model_validate(user).model_dump()
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'teste@mail.com',
            'password': 'senha123',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_email_already_created(client, user):
    response = client.post(
        '/users',
        json={'username': 'nome', 'email': user.email, 'password': 'password'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):

    user_schema = UserPublic.model_validate(user).model_dump()
    # transforma a classe do SQLAlchemy num schema do pydantic

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_one_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_read_one_user_not_found(client):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


#  estavam ruins os antigos testes. CODE SMELL:
# - O usuário era lido em test_read_users é o mesmo criado em test_create_user
# - Portanto, eles dependiam da ordem de execução
# - se eu rodasse só o test_read_users, ele ia falhar


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.json() == {'message': 'User deleted'}


def test_update_not_found(client):
    response = client.put(
        '/users/2',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_not_found(client):
    response = client.delete('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
