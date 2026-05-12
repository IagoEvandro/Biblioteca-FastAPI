from pydantic import BaseModel, field_validator
from datetime import date

class Livro(BaseModel):
    tipo: str
    data_publicacao: date
    preco: float
    
    @field_validator("data_publicacao")
    def auth_data(cls, v):
     if v > date.today():
        raise ValueError("Data não pode ser no futuro")
     return v
  
class GeneroRequest(BaseModel):
    genero: str