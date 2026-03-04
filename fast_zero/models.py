from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()  # registra metadados


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    # init false é pra não inicializar o id, quem faz isso é o banco de dados
    # init false não é obrigatório, mas ser explícito é melhor q serimplícito
    # primary key já faz autoincrement por padrão
    username: Mapped[str] = mapped_column(unique=True)
    # usernames têm que ser únicos, não podem ser repetidos
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    # emails tbm têm que ser únicos, não podem ser repetidos
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )  # o tempo do servidor é quem vai decidir
    updated_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now(), server_default=func.now()
    )
    # os valores None serão preenchidos quando houver comunicação com o banco
