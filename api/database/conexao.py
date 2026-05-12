import os

import aiomysql


def _get_required_env(nome: str) -> str:
    valor = os.getenv(nome)
    if not valor:
        raise RuntimeError(f"Variavel de ambiente obrigatoria nao configurada: {nome}")
    return valor


async def get_connection():
    return await aiomysql.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=_get_required_env("MYSQL_USER"),
        password=_get_required_env("MYSQL_PASSWORD"),
        db=os.getenv("MYSQL_DATABASE", "biblioteca_api"),
        autocommit=False,
    )
