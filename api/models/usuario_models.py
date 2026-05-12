from pydantic import BaseModel, field_validator

class LoginRequest(BaseModel):
    username: str
    senha: str

class Usuario(BaseModel):
    nome: str
    username: str
    email: str
    
    
class UsuarioCreate(BaseModel):
    nome: str
    username: str
    email: str
    senha: str
    
    @field_validator("senha")
    def auth_senha(cls, v):
        if len(v) < 8:
            raise ValueError("Senha deve ter pelo menos 8 caracteres")
        return v
    
class UsuarioResponse(BaseModel):
    id: int
    nome: str
    username: str
    email: str  


class UsuarioUpdate(BaseModel):
    nome: str
    username: str
    email: str
    senha: str

    @field_validator("senha")
    def auth_senha(cls, v):
        if len(v) < 8:
            raise ValueError("Senha deve ter pelo menos 8 caracteres")
        return v


  
