from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    model_config = ConfigDict(from_attributes=True)


class UserPublic(BaseModel):  # pra não aparecer a senha na resposta
    username: str
    email: EmailStr
    id: int
    model_config = ConfigDict(from_attributes=True)
    # pra model_validate ler os atributos da classe
    # vai tentar validar os atributos q tem os nomes dos atributos do schema


class UserDB(UserSchema):
    id: int


class UserList(BaseModel):
    users: list[UserPublic]
