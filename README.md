# Biblioteca-FastAPI

# Documentacao Geral do Projeto Biblioteca API

Este documento descreve todo o projeto atual da API de biblioteca, incluindo estrutura de pastas, dependencias, configuracao, banco de dados, seguranca, models, services e rotas.

## 1. Visao geral

O projeto e uma API REST feita com FastAPI para gerenciar recursos de uma biblioteca.

Recursos implementados:

- usuarios;
- login com JWT;
- livros;
- generos;
- enderecos.

Recursos parcialmente presentes:

- autores possuem model, mas ainda nao possuem rotas nem metodos no service.

## 2. Estrutura de arquivos

Estrutura principal:

```text
api/
  database/
    biblioteca.sql
    conexao.py
  main/
    main.py
  models/
    autor_models.py
    endereco_models.py
    genero_models.py
    livro_models.py
    usuario_models.py
  routes/
    endereco_routes.py
    livro_routes.py
    usuario_routes.py
  security/
    jwt_config.py
  services/
    biblioteca_service.py
docs/
  crud_usuarios.md
  projeto_biblioteca_api.md
requirements.txt
```

## 3. Dependencias

Arquivo: `requirements.txt`

```text
fastapi
uvicorn
python-jose
python-multipart
aiomysql
```

Finalidade de cada dependencia:

- `fastapi`: framework principal da API.
- `uvicorn`: servidor ASGI usado para executar o FastAPI.
- `python-jose`: biblioteca usada para criar e validar tokens JWT.
- `python-multipart`: necessario para o `OAuth2PasswordRequestForm` usado no login.
- `aiomysql`: driver assincrono para conectar a API ao MySQL sem bloquear o event loop.

## 4. Execucao do projeto

Com a `.venv` ativada, uma forma comum de iniciar a API e:

```powershell
.\.venv\Scripts\python.exe -m uvicorn api.main.main:app --reload
```

Depois, a documentacao interativa fica disponivel em:

```text
http://localhost:8000/docs
```

## 5. Arquivo principal

Arquivo: `api/main/main.py`

Responsabilidade:

- criar a aplicacao FastAPI;
- registrar os routers de usuarios, livros e enderecos.

Codigo atual:

```python
from fastapi import FastAPI
from api.routes.usuario_routes import router as usuario_router
from api.routes.livro_routes import router as livro_router
from api.routes.endereco_routes import router as endereco_router

app = FastAPI()

app.include_router(usuario_router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(livro_router, prefix="/livros", tags=["Livros"])
app.include_router(endereco_router, prefix="/enderecos", tags=["Enderecos"])
```

Prefixos finais:

- rotas de usuarios comecam com `/usuarios`;
- rotas de livros comecam com `/livros`;
- rotas de enderecos comecam com `/enderecos`.

## 6. Configuracao do banco

Arquivo: `api/database/conexao.py`

Responsabilidade:

- criar conexoes com o banco MySQL.

Codigo atual:

```python
import os

import aiomysql


async def get_connection():
    return await aiomysql.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "1234"),
        database=os.getenv("MYSQL_DATABASE", "biblioteca_api"),
        autocommit=False,
    )
```

Variaveis de ambiente aceitas:

- `MYSQL_HOST`, padrao `localhost`;
- `MYSQL_PORT`, padrao `3306`;
- `MYSQL_USER`, padrao `root`;
- `MYSQL_PASSWORD`, padrao `1234`;
- `MYSQL_DATABASE`, padrao `biblioteca_api`.

## 7. Banco de dados

Arquivo: `api/database/biblioteca.sql`

O script cria o banco:

```sql
CREATE DATABASE IF NOT EXISTS biblioteca_api
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

### Tabela `usuarios`

```sql
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha_hash CHAR(64) NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Observacoes:

- `username` e unico.
- `email` e unico.
- `senha_hash` guarda a senha em formato SHA-256.

### Tabela `generos`

```sql
CREATE TABLE IF NOT EXISTS generos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(80) NOT NULL UNIQUE,
    disponivel BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabela `livros`

```sql
CREATE TABLE IF NOT EXISTS livros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(120) NOT NULL UNIQUE,
    data_publicacao DATE NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_livros_preco CHECK (preco >= 0),
    CONSTRAINT chk_livros_data CHECK (data_publicacao <= CURRENT_DATE)
);
```

Regras:

- `tipo` e unico.
- `preco` nao pode ser negativo.
- `data_publicacao` nao pode estar no futuro.

### Tabela `enderecos`

```sql
CREATE TABLE IF NOT EXISTS enderecos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    logradouro VARCHAR(150) NOT NULL,
    numero INT NOT NULL,
    bairro VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado CHAR(2) NOT NULL,
    cep CHAR(8) NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_enderecos_cep CHECK (cep REGEXP '^[0-9]{8}$')
);
```

Regra:

- `cep` deve ter 8 digitos numericos.

## 8. Seguranca e JWT

Arquivo: `api/security/jwt_config.py`

Responsabilidades:

- configurar o esquema OAuth2;
- criar tokens JWT;
- validar tokens JWT nas rotas protegidas.

Configuracoes atuais:

```python
SECRET_KEY = "troque_esta_chave_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

O token e obtido em:

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/login")
```

Funcao para criar token:

```python
def criar_token(dados: dict):
    dados_para_token = dados.copy()
    expiracao = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    dados_para_token.update({"exp": expiracao})

    return jwt.encode(dados_para_token, SECRET_KEY, algorithm=ALGORITHM)
```

Funcao para validar token:

```python
def verificar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Token invalido")

        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalido ou expirado")
```

Rotas protegidas usam:

```python
usuario: str = Depends(verificar_token)
```

## 9. Models

Os models usam Pydantic e ficam em `api/models`.

### Usuario

Arquivo: `api/models/usuario_models.py`

Classes:

```python
class LoginRequest(BaseModel):
    username: str
    senha: str
```

Observacao:

- Existe no projeto, mas a rota de login usa `OAuth2PasswordRequestForm`.

```python
class Usuario(BaseModel):
    nome: str
    username: str
    email: str
```

```python
class UsuarioCreate(BaseModel):
    nome: str
    username: str
    email: str
    senha: str
```

Valida senha com pelo menos 8 caracteres.

```python
class UsuarioResponse(BaseModel):
    id: int
    nome: str
    username: str
    email: str
```

```python
class UsuarioUpdate(BaseModel):
    nome: str
    username: str
    email: str
    senha: str
```

Tambem valida senha com pelo menos 8 caracteres.

### Livro

Arquivo: `api/models/livro_models.py`

```python
class Livro(BaseModel):
    tipo: str
    data_publicacao: date
    preco: float
```

Validacao:

- `data_publicacao` nao pode estar no futuro.

```python
class GeneroRequest(BaseModel):
    genero: str
```

Usado para cadastrar generos pela rota de livros.

### Genero

Arquivo: `api/models/genero_models.py`

```python
class Genero(BaseModel):
    nome: str
```

Validacao:

- remove espacos no inicio e no fim;
- converte para minusculo.

Observacao:

- Esse model existe, mas as rotas atuais usam `GeneroRequest` de `livro_models.py`.

### Endereco

Arquivo: `api/models/endereco_models.py`

```python
class Endereco(BaseModel):
    logradouro: str
    numero: int
    bairro: str
    cidade: str
    estado: str
    cep: str
```

Validacao:

- aceita CEP com ou sem hifen;
- remove `-`;
- exige 8 digitos numericos.

### Autor

Arquivo: `api/models/autor_models.py`

```python
class Autor(BaseModel):
    nome: str
```

Observacao:

- O model existe, mas nao ha rotas ou metodos de service para autores no estado atual do projeto.

## 10. Service principal

Arquivo: `api/services/biblioteca_service.py`

O projeto concentra as regras de acesso ao banco em uma classe:

```python
class BibliotecaService:
```

Esse service e usado pelas rotas:

```python
service = BibliotecaService()
```

Os metodos que acessam o banco sao `async` e devem ser chamados com `await` nas rotas. Isso evita que consultas MySQL bloqueiem o event loop do FastAPI.

### Usuarios

Metodos:

- `gerar_hash_senha(senha: str)`;
- `login(usuario, senha)`;
- `cadastrar_usuario(usuario)`;
- `listar_usuarios()`;
- `buscar_usuario(usuario_id: int)`;
- `atualizar_usuario(usuario_id: int, usuario)`;
- `deletar_usuario(usuario_id: int)`.

Pontos importantes:

- senhas sao convertidas para SHA-256;
- listagem e busca nao retornam `senha_hash`;
- conflitos de `username` ou `email` retornam `None` em cadastro e atualizacao;
- deletar e atualizar usam `cursor.rowcount > 0` para saber se o registro existia.

### Generos

Metodos:

- `livros_disponiveis(livro)`;
- `livros_indisponiveis(livro)`;
- `adicionar_genero(genero)`.

Observacao:

- Apesar do nome `livros_disponiveis`, o metodo consulta a tabela `generos`.
- `adicionar_genero` trata duplicidade com `IntegrityError`.

### Livros

Metodos:

- `cadastro_livro(livro)`;
- `listar_livros()`;
- `buscar_livro(livro_id: int)`;
- `atualizar_livro(livro_id: int, livro)`;
- `deletar_livro(livro_id: int)`.

Pontos importantes:

- `tipo` e normalizado com `strip().lower()` no cadastro e atualizacao;
- duplicidade no cadastro retorna `False`;
- busca e listagem retornam `id`, `tipo`, `data_publicacao` e `preco`.

### Enderecos

Metodos:

- `cadastrar_endereco(endereco)`;
- `listar_enderecos()`;
- `buscar_endereco(endereco_id: int)`;
- `atualizar_endereco(endereco_id: int, endereco)`;
- `deletar_endereco(endereco_id: int)`.

Pontos importantes:

- `estado` e salvo em maiusculo;
- `cep` ja chega validado pelo model;
- cadastro retorna `cursor.lastrowid`.

## 11. Rotas de usuarios

Arquivo: `api/routes/usuario_routes.py`

Prefixo no `main.py`:

```text
/usuarios
```

### `POST /usuarios/login`

Autentica usuario e retorna token JWT.

Campos:

- `username`;
- `password`.

Resposta:

```json
{
    "access_token": "token",
    "token_type": "bearer"
}
```

### `POST /usuarios`

Cadastra usuario.

Body:

```json
{
    "nome": "Maria Silva",
    "username": "maria",
    "email": "maria@email.com",
    "senha": "senha1234"
}
```

Resposta:

```json
{
    "id": 3,
    "mensagem": "Usuario cadastrado com sucesso"
}
```

### `GET /usuarios`

Lista usuarios.

Requer JWT.

### `GET /usuarios/{usuario_id}`

Busca usuario por ID.

Requer JWT.

### `PUT /usuarios/{usuario_id}`

Atualiza usuario.

Requer JWT.

### `DELETE /usuarios/{usuario_id}`

Remove usuario.

Requer JWT.

## 12. Rotas de livros e generos

Arquivo: `api/routes/livro_routes.py`

Prefixo no `main.py`:

```text
/livros
```

### `GET /livros/generos/disponiveis/{genero}`

Verifica se um genero esta disponivel.

Resposta:

```json
{
    "genero": "romance",
    "disponivel": true
}
```

Essa rota nao exige token.

### `POST /livros/generos`

Adiciona um genero.

Requer JWT.

Body:

```json
{
    "genero": "fantasia"
}
```

Resposta quando cadastra:

```json
{
    "mensagem": "Genero adicionado com sucesso!!",
    "usuario": "admin"
}
```

Resposta quando ja existe:

```json
{
    "mensagem": "Genero ja adicionado!!"
}
```

### `POST /livros`

Cadastra livro.

Requer JWT.

Body:

```json
{
    "tipo": "romance",
    "data_publicacao": "2024-01-10",
    "preco": 49.9
}
```

Resposta quando cadastra:

```json
{
    "mensagem": "Livro cadastrado com sucesso!!",
    "usuario": "admin"
}
```

Resposta quando ja existe:

```json
{
    "mensagem": "Livro ja adicionado"
}
```

### `GET /livros`

Lista livros.

Nao exige token.

### `GET /livros/{livro_id}`

Busca livro por ID.

Nao exige token.

Erro quando nao encontra:

```json
{
    "detail": "Livro nao encontrado"
}
```

### `PUT /livros/{livro_id}`

Atualiza livro.

Requer JWT.

### `DELETE /livros/{livro_id}`

Remove livro.

Requer JWT.

## 13. Rotas de enderecos

Arquivo: `api/routes/endereco_routes.py`

Prefixo no `main.py`:

```text
/enderecos
```

### `POST /enderecos`

Cadastra endereco.

Requer JWT.

Body:

```json
{
    "logradouro": "Rua A",
    "numero": 123,
    "bairro": "Centro",
    "cidade": "Sao Paulo",
    "estado": "sp",
    "cep": "01001-000"
}
```

Resposta:

```json
{
    "id": 1,
    "mensagem": "Endereco cadastrado com sucesso",
    "endereco": {
        "logradouro": "Rua A",
        "numero": 123,
        "bairro": "Centro",
        "cidade": "Sao Paulo",
        "estado": "sp",
        "cep": "01001000"
    },
    "usuario": "admin"
}
```

### `GET /enderecos`

Lista enderecos.

Nao exige token.

### `GET /enderecos/{endereco_id}`

Busca endereco por ID.

Nao exige token.

### `PUT /enderecos/{endereco_id}`

Atualiza endereco.

Requer JWT.

### `DELETE /enderecos/{endereco_id}`

Remove endereco.

Requer JWT.

## 14. Rotas publicas e protegidas

Rotas publicas:

- `POST /usuarios/login`;
- `POST /usuarios`;
- `GET /livros/generos/disponiveis/{genero}`;
- `GET /livros`;
- `GET /livros/{livro_id}`;
- `GET /enderecos`;
- `GET /enderecos/{endereco_id}`.

Rotas protegidas por JWT:

- `GET /usuarios`;
- `GET /usuarios/{usuario_id}`;
- `PUT /usuarios/{usuario_id}`;
- `DELETE /usuarios/{usuario_id}`;
- `POST /livros/generos`;
- `POST /livros`;
- `PUT /livros/{livro_id}`;
- `DELETE /livros/{livro_id}`;
- `POST /enderecos`;
- `PUT /enderecos/{endereco_id}`;
- `DELETE /enderecos/{endereco_id}`.

## 15. Fluxo de uso no Swagger

1. Inicie a API.
2. Acesse:

```text
http://localhost:8000/docs
```

3. Cadastre um usuario em `POST /usuarios`.
4. Faca login em `POST /usuarios/login`.
5. Copie o `access_token`.
6. Clique em `Authorize`.
7. Informe o token.
8. Teste as rotas protegidas.

No Swagger, informe o token no formato:

```text
Bearer seu_token_aqui
```

## 16. Observacoes importantes sobre o estado atual

### Senhas iniciais do SQL

O script SQL insere:

```sql
('Administrador', 'admin', 'admin@email.com', SHA2('1234', 256)),
('Iago', 'iago', 'iago@email.com', SHA2('senha123', 256))
```

Mas o model da API exige senha com pelo menos 8 caracteres em cadastro e atualizacao.

Impacto:

- o usuario `admin` pode existir no banco com senha `1234`;
- a API nao permite cadastrar novos usuarios com senha menor que 8 caracteres.

### Textos com acentuacao

Algumas mensagens aparecem com caracteres quebrados em arquivos atuais, como:

```text
Data nÃ£o pode ser no futuro
CEP invÃ¡lido
```

Isso parece ser um problema de encoding nos arquivos.

### Autor ainda nao tem CRUD

Existe:

```text
api/models/autor_models.py
```

Mas ainda nao existe:

- `api/routes/autor_routes.py`;
- metodos de autor em `BibliotecaService`;
- tabela `autores` no SQL atual.

## 17. Validacoes recomendadas

Validar sintaxe:

```powershell
.\.venv\Scripts\python.exe -m compileall api
```

Verificar rotas de usuarios:

```powershell
.\.venv\Scripts\python.exe -c "from api.main.main import app; print([(route.path, sorted(route.methods)) for route in app.routes if 'usuarios' in route.path])"
```

Verificar todas as rotas principais:

```powershell
.\.venv\Scripts\python.exe -c "from api.main.main import app; print([(route.path, sorted(route.methods)) for route in app.routes])"
```

## 18. Resumo dos endpoints

### Usuarios

```text
POST   /usuarios/login
POST   /usuarios
GET    /usuarios
GET    /usuarios/{usuario_id}
PUT    /usuarios/{usuario_id}
DELETE /usuarios/{usuario_id}
```

### Livros e generos

```text
GET    /livros/generos/disponiveis/{genero}
POST   /livros/generos
POST   /livros
GET    /livros
GET    /livros/{livro_id}
PUT    /livros/{livro_id}
DELETE /livros/{livro_id}
```

### Enderecos

```text
POST   /enderecos
GET    /enderecos
GET    /enderecos/{endereco_id}
PUT    /enderecos/{endereco_id}
DELETE /enderecos/{endereco_id}
```
