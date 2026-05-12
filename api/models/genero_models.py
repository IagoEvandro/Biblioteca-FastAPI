from pydantic import BaseModel,field_validator

class Genero(BaseModel):
    nome: str
    
    @field_validator("nome")
    def padronizar_nome(cls, v):
        return v.strip().lower()