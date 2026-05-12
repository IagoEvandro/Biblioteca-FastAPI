from fastapi import APIRouter, Depends, HTTPException
from api.security.jwt_config import verificar_token
from api.services.biblioteca_service import BibliotecaService
from api.models.endereco_models import Endereco

router = APIRouter()
service = BibliotecaService()

@router.post("")
async def cadastrar_endereco(
    endereco: Endereco,
    usuario: str = Depends(verificar_token)
):
    endereco_id = await service.cadastrar_endereco(endereco)

    return {
        "id": endereco_id,
        "mensagem": "Endereco cadastrado com sucesso",
        "endereco": endereco,
        "usuario": usuario
    }
    
@router.get("")
async def listar_enderecos():
    return await service.listar_enderecos()

@router.get("/{endereco_id}")
async def buscar_endereco(endereco_id: int):
    endereco = await service.buscar_endereco(endereco_id)

    if not endereco:
        raise HTTPException(status_code=404, detail="Endereco nao encontrado")
    
    return{
        "mensagem": "Endereco encontrado com sucesso",
        "endereco": endereco
    }
    
@router.put("/{endereco_id}")
async def atualizar_endereco(
    endereco_id: int,
    endereco: Endereco,
    usuario: str = Depends(verificar_token)
):
    atualizado = await service.atualizar_endereco(endereco_id, endereco)

    if not atualizado:
        raise HTTPException(status_code=404, detail="Endereco nao encontrado")
    
    return{
        "mensagem": "Endereco atualizado com sucesso",
        "endereco": endereco,
        "usuario": usuario
    }
    
@router.delete("/{endereco_id}")
async def deletar_endereco(
    endereco_id: int,
    usuario: str = Depends(verificar_token)
):
    deletado = await service.deletar_endereco(endereco_id)

    if not deletado:
        raise HTTPException(status_code=404, detail="Endereco nao encontrado")
    
    return{
        "mensagem": "Endereco deletado com sucesso",
        "usuario": usuario
    }
