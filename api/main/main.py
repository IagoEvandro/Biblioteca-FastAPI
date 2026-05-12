from fastapi import FastAPI
from api.routes.usuario_routes import router as usuario_router
from api.routes.livro_routes import router as livro_router
from api.routes.endereco_routes import router as endereco_router

app = FastAPI()

app.include_router(usuario_router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(livro_router, prefix="/livros", tags=["Livros"])
app.include_router(endereco_router, prefix="/enderecos", tags=["Enderecos"])

