from fastapi import APIRouter, Depends, HTTPException
from api.models.livro_models import GeneroRequest, Livro
from api.security.jwt_config import verificar_token
from api.services.biblioteca_service import BibliotecaService

router = APIRouter()
service = BibliotecaService()

@router.get("/generos/disponiveis/{genero}")
async def verificar_genero_disponivel(genero: str):
    disponivel = await service.livros_disponiveis(genero)
    return {"genero": genero, "disponivel": disponivel}


@router.post("/generos")
async def adicionar_genero(dados: GeneroRequest, usuario: str = Depends(verificar_token)):
    adicionado = await service.adicionar_genero(dados.genero)
    
    if adicionado:
        return{"mensagem": "Genero adicionado com sucesso!!", "usuario": usuario}
    
    return{"mensagem": "Genero ja adicionado!!"}

@router.post("")
async def cadastro_livro(livro: Livro, usuario: str = Depends(verificar_token)):
    cadastrado = await service.cadastro_livro(livro)
    
    if cadastrado:
        return{"mensagem": "Livro cadastrado com sucesso!!", "usuario": usuario}
    
    return{"mensagem": "Livro ja adicionado"}

@router.get ("")
async def listar_livros():
    return await service.listar_livros()

@router.get("/{livro_id}")
async def buscar_livro(livro_id: int):
    livro = await service.buscar_livro(livro_id)

    if not livro:
        raise HTTPException(status_code=404, detail="Livro nao encontrado")
    
    return {
        "mensagem": "Livro encontrado com sucesso",
        "livro": livro
    }

@router.put("/{livro_id}")
async def atualizar_livro(
    livro_id: int,
    livro: Livro,
    usuario: str = Depends(verificar_token)
):
    atualizado = await service.atualizar_livro(livro_id, livro)

    if not atualizado:
        raise HTTPException(status_code=404, detail="Livro nao encontrado")

    return {
        "mensagem": "Livro atualizado com sucesso",
        "usuario": usuario
    }

@router.delete("/{livro_id}")
async def deletar_livro(livro_id: int, usuario: str = Depends(verificar_token)):
    deletado = await service.deletar_livro(livro_id)

    if not deletado:
        raise HTTPException(status_code=404, detail="Livro nao encontrado")

    return {
        "mensagem": "Livro deletado com sucesso",
        "usuario": usuario
    }
