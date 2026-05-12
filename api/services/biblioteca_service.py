import hashlib

import aiomysql
from pymysql.err import IntegrityError

from api.database.conexao import get_connection


class BibliotecaService:
    def gerar_hash_senha(self, senha: str):
        return hashlib.sha256(senha.encode()).hexdigest()

    async def login(self, usuario, senha):
        usuario = usuario.strip().lower()
        senha = senha.strip()
        senha_hash = self.gerar_hash_senha(senha)

        conexao = await get_connection()

        try:
            async with conexao.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    """
                    SELECT id
                    FROM usuarios
                    WHERE LOWER(username) = %s AND senha_hash = %s
                    """,
                    (usuario, senha_hash),
                )
                usuario_encontrado = await cursor.fetchone()

            return usuario_encontrado is not None
        finally:
            conexao.close()

    async def cadastrar_usuario(self, usuario):
        conexao = await get_connection()
        senha_hash = self.gerar_hash_senha(usuario.senha.strip())

        try:
            async with conexao.cursor() as cursor:
                await cursor.execute(
                    """
                    INSERT INTO usuarios (nome, username, email, senha_hash)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        usuario.nome.strip(),
                        usuario.username.strip().lower(),
                        usuario.email.strip().lower(),
                        senha_hash,
                    ),
                )
                await conexao.commit()
                return cursor.lastrowid
        except IntegrityError:
            await conexao.rollback()
            return None
        finally:
            conexao.close()

    async def listar_usuarios(self):
        conexao = await get_connection()

        try:
            async with conexao.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    """
                    SELECT id, nome, username, email
                    FROM usuarios
                    ORDER BY id
                    """
                )
                return await cursor.fetchall()
        finally:
            conexao.close()

    async def buscar_usuario(self, usuario_id: int):
        conexao = await get_connection()

        try:
            async with conexao.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    """
                    SELECT id, nome, username, email
                    FROM usuarios
                    WHERE id = %s
                    """,
                    (usuario_id,),
                )
                return await cursor.fetchone()
        finally:
            conexao.close()

    async def atualizar_usuario(self, usuario_id: int, usuario):
        conexao = await get_connection()
        senha_hash = self.gerar_hash_senha(usuario.senha.strip())

        try:
            async with conexao.cursor() as cursor:
                await cursor.execute(
                    """
                    UPDATE usuarios
                    SET nome = %s,
                        username = %s,
                        email = %s,
                        senha_hash = %s
                    WHERE id = %s
                    """,
                    (
                        usuario.nome.strip(),
                        usuario.username.strip().lower(),
                        usuario.email.strip().lower(),
                        senha_hash,
                        usuario_id,
                    ),
                )
                await conexao.commit()
                return cursor.rowcount > 0
        except IntegrityError:
            await conexao.rollback()
            return None
        finally:
            conexao.close()

    async def deletar_usuario(self, usuario_id: int):
        conexao = await get_connection()

        try:
            async with conexao.cursor() as cursor:
                await cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
                await conexao.commit()
                return cursor.rowcount > 0
        finally:
            conexao.close()

    async def livros_disponiveis(self, livro):
        livro = livro.strip().lower()
        conexao = await get_connection()

        try:
            async with conexao.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    """
                    SELECT disponivel
                    FROM generos
                    WHERE nome = %s
                    """,
                    (livro,),
                )
                genero = await cursor.fetchone()

            return bool(genero and genero["disponivel"])
        finally:
            conexao.close()

    async def livros_indisponiveis(self, livro):
        return not await self.livros_disponiveis(livro)

    async def adicionar_genero(self, genero):
        genero = genero.strip().lower()
        conexao = await get_connection()

        try:
            async with conexao.cursor() as cursor:
                await cursor.execute(
                    """
                    INSERT INTO generos (nome, disponivel)
                    VALUES (%s, TRUE)
                    """,
                    (genero,),
                )
                await conexao.commit()
                return True
        except IntegrityError:
            await conexao.rollback()
            return False
        finally:
            conexao.close()

    async def cadastro_livro(self, livro):
        conexao = await get_connection()

        try:
            async with conexao.cursor() as cursor:
                await cursor.execute(
                    """
                    INSERT INTO livros (tipo, data_publicacao, preco)
                    VALUES (%s, %s, %s)
                    """,
                    (livro.tipo.strip().lower(), livro.data_publicacao, livro.preco),
                )
                await conexao.commit()
                return True
        except IntegrityError:
            await conexao.rollback()
            return False
        finally:
            conexao.close()

    async def listar_livros(self):
        conexao = await get_connection()

        try:
            async with conexao.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    """
                    SELECT id, tipo, data_publicacao, preco
                    FROM livros
                    ORDER BY id
                    """
                )
                return await cursor.fetchall()
        finally:
            conexao.close()

    async def buscar_livro(self, livro_id: int):
        conexao = await get_connection()

        try:
            async with conexao.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    """
                    SELECT id, tipo, data_publicacao, preco
                    FROM livros
                    WHERE id = %s
                    """,
                    (livro_id,),
                )
                return await cursor.fetchone()
        finally:
            conexao.close()

    async def atualizar_livro(self, livro_id: int, livro):
        conexao = await get_connection()

        try:
            async with conexao.cursor() as cursor:
                await cursor.execute(
                    """
                    UPDATE livros
                    SET tipo = %s, data_publicacao = %s, preco = %s
                    WHERE id = %s
                    """,
                    (livro.tipo.strip().lower(), livro.data_publicacao, livro.preco, livro_id),
                )
                await conexao.commit()
                return cursor.rowcount > 0
        finally:
            conexao.close()

    async def deletar_livro(self, livro_id: int):
        conexao = await get_connection()

        try:
            async with conexao.cursor() as cursor:
                await cursor.execute("DELETE FROM livros WHERE id = %s", (livro_id,))
                await conexao.commit()
                return cursor.rowcount > 0
        finally:
            conexao.close()

    async def cadastrar_endereco(self, endereco):
        conexao = await get_connection()

        try:
            async with conexao.cursor() as cursor:
                await cursor.execute(
                    """
                    INSERT INTO enderecos (
                        logradouro, numero, bairro, cidade, estado, cep
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        endereco.logradouro,
                        endereco.numero,
                        endereco.bairro,
                        endereco.cidade,
                        endereco.estado.upper(),
                        endereco.cep,
                    ),
                )
                await conexao.commit()
                return cursor.lastrowid
        finally:
            conexao.close()

    async def listar_enderecos(self):
        conexao = await get_connection()

        try:
            async with conexao.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    """
                    SELECT id, logradouro, numero, bairro, cidade, estado, cep
                    FROM enderecos
                    ORDER BY id
                    """
                )
                return await cursor.fetchall()
        finally:
            conexao.close()

    async def buscar_endereco(self, endereco_id: int):
        conexao = await get_connection()

        try:
            async with conexao.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    """
                    SELECT id, logradouro, numero, bairro, cidade, estado, cep
                    FROM enderecos
                    WHERE id = %s
                    """,
                    (endereco_id,),
                )
                return await cursor.fetchone()
        finally:
            conexao.close()

    async def atualizar_endereco(self, endereco_id: int, endereco):
        conexao = await get_connection()

        try:
            async with conexao.cursor() as cursor:
                await cursor.execute(
                    """
                    UPDATE enderecos
                    SET logradouro = %s,
                        numero = %s,
                        bairro = %s,
                        cidade = %s,
                        estado = %s,
                        cep = %s
                    WHERE id = %s
                    """,
                    (
                        endereco.logradouro,
                        endereco.numero,
                        endereco.bairro,
                        endereco.cidade,
                        endereco.estado.upper(),
                        endereco.cep,
                        endereco_id,
                    ),
                )
                await conexao.commit()
                return cursor.rowcount > 0
        finally:
            conexao.close()

    async def deletar_endereco(self, endereco_id: int):
        conexao = await get_connection()

        try:
            async with conexao.cursor() as cursor:
                await cursor.execute("DELETE FROM enderecos WHERE id = %s", (endereco_id,))
                await conexao.commit()
                return cursor.rowcount > 0
        finally:
            conexao.close()
