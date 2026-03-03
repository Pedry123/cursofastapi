import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.models import table_registry


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    # banco em memória pra conseguir fazer os testes
    # e apagar quando acabar o teste
    table_registry.metadata.create_all(engine)

    # gerenciamento de contexto
    with Session(engine) as session:
        yield session  # transforma em um generator
    # ele para de executar aqui e vai lá pra função de teste

    table_registry.metadata.drop_all(engine)  # tear down
