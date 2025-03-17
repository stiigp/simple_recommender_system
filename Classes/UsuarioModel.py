from pydantic import BaseModel

class UsuarioModel(BaseModel):
    username: str
    email: str
    password: str