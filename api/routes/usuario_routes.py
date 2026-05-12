from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from api.models.usuario_models import UsuarioCreate, UsuarioUpdate
from api.services.biblioteca_service import BibliotecaService
from api.security.jwt_config import criar_token, verificar_token

router = APIRouter()
service = BibliotecaService()


@router.post("/login")
async def login(dados: OAuth2PasswordRequestForm = Depends()):

    sucesso = await service.login(dados.username, dados.password)

    if not sucesso:
        raise HTTPException(
            status_code=401,
            detail="Usuario ou senha invalidos!!"
        )

    token = criar_token({"sub": dados.username})

    return {"access_token": token, "token_type": "bearer"}


@router.post("")
async def adicionar_usuario(dados: UsuarioCreate):
    usuario_id = await service.cadastrar_usuario(dados)

    if not usuario_id:
        raise HTTPException(
            status_code=400,
            detail="Username ou email ja cadastrado"
        )

    return {
        "id": usuario_id,
        "mensagem": "Usuario cadastrado com sucesso"
    }


@router.get("")
async def listar_usuarios(usuario: str = Depends(verificar_token)):
    return await service.listar_usuarios()


@router.get("/{usuario_id}")
async def buscar_usuario(usuario_id: int, usuario: str = Depends(verificar_token)):
    usuario_encontrado = await service.buscar_usuario(usuario_id)

    if not usuario_encontrado:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")

    return {
        "mensagem": "Usuario encontrado com sucesso",
        "usuario": usuario_encontrado
    }


@router.put("/{usuario_id}")
async def atualizar_usuario(
    usuario_id: int,
    dados: UsuarioUpdate,
    usuario: str = Depends(verificar_token)
):

    atualizado = await service.atualizar_usuario(usuario_id, dados)

    if atualizado is None:
        raise HTTPException(
            status_code=400,
            detail="Username ou email ja cadastrado"
        )

    if not atualizado:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")

    return {
        "mensagem": "Usuario atualizado com sucesso",
        "usuario": usuario
    }


@router.delete("/{usuario_id}")
async def deletar_usuario(
    usuario_id: int,
    usuario: str = Depends(verificar_token)
):

    deletado = await service.deletar_usuario(usuario_id)

    if not deletado:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")

    return {
        "mensagem": "Usuario deletado com sucesso",
        "usuario": usuario
    }
