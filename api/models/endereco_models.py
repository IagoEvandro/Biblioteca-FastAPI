from pydantic import BaseModel, field_validator

class Endereco(BaseModel):
    logradouro: str
    numero: int
    bairro: str
    cidade: str
    estado: str
    cep: str
    
    @field_validator("cep")
    def auth_cep(cls, v):
        v = v.replace("-", "")
        if len(v) != 8 or not v.isdigit():
            raise ValueError("CEP inválido")
        return v
    