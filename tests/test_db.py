from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(username='pedro', email='pedro@email.com', password='senha123')

    session.add(user)
    session.commit()

    result = session.scalar(
        select(User).where(User.email == 'pedro@email.com')
    )
    # scalar me retorna o registro do banco de dados
    # no formato de um objeto python
    # session.refresh(user)
    # refresh é pra sincronizar com o objeto do banco
    # ex: add id e created_at

    assert result.username == 'pedro'
