import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

# StaticPool pra não criar validações e coisas mais complexas
# Antes, ele usa o mesmo recurso, o básico, só pro teste
# threads vão usar o mesmo canal de comunicação
# Específico do SQLite essas questões
from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import User, table_registry


@pytest.fixture
def client(session):

    def get_test_session():
        return session

    app.dependency_overrides[get_session] = get_test_session
    with TestClient(app) as client:
        # vai trocar o depends lá de app.py (produção) pra um de teste
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
        # pool=StaticPool() tbm vai
    )
    # banco em memória pra conseguir fazer os testes
    # e apagar quando acabar o teste
    table_registry.metadata.create_all(engine)

    # gerenciamento de contexto

    with Session(engine) as session:
        yield session  # transforma em um generator
    # ele para de executar aqui e vai lá pra função de teste

    table_registry.metadata.drop_all(engine)  # tear down
    engine.dispose()


@pytest.fixture
def user(session):
    user = User(username='Teste', email='teste@test.com', password='testest')

    session.add(user)
    session.commit()
    session.refresh(user)
    return user
