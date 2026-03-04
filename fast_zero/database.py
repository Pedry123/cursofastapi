from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.settings import Settings

engine = create_engine(Settings().DATABASE_URL)


# pragma no cover é só pra funções que
# NÃO PODEM SER TESTADAS!!!!
# é o caso de get_session porque nos testes
# sobrescrevemos a session por uma session de teste
# irrelevante: só vai testar a conexão da engine
def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session
        # sem o yield, a sessão não seria
        # fechada corretamente
