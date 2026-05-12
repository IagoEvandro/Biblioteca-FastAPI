# Biblioteca API - Documentacao Tecnica

## 1. Objetivo

Este documento apresenta a visao tecnica da Biblioteca API, uma API REST desenvolvida com FastAPI para gerenciamento de recursos de biblioteca.

O conteudo foi estruturado para uso interno em ambiente corporativo e nao deve conter credenciais, tokens, senhas, dados pessoais reais ou qualquer informacao sensivel. Exemplos de payload usam dados ficticios e placeholders.

## 2. Escopo Funcional

Recursos implementados:

- usuarios;
- autenticacao com JWT;
- livros;
- generos;
- enderecos.

Recursos parcialmente implementados:

- autores possuem model, mas ainda nao possuem tabela, rotas ou metodos no service.

## 3. Estrutura do Projeto

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
  projeto_biblioteca_api.md
  postman_collection_biblioteca_api.json
requirements.txt
```

## 4. Dependencias

Arquivo: `requirements.txt`

```text
fastapi
uvicorn
python-jose
python-multipart
aiomysql
```

Finalidade:

- `fastapi`: framework principal da API.
- `uvicorn`: servidor ASGI.
- `python-jose`: criacao e validacao de tokens JWT.
- `python-multipart`: suporte ao formulario OAuth2 usado no login.
- `aiomysql`: driver assincrono para conexao com MySQL.

## 5. Execucao Local

Com a `.venv` ativada, execute:

```powershell
.\.venv\Scripts\python.exe -m uvicorn api.main.main:app --reload
```

Documentacao interativa:

```text
http://localhost:8000/docs
```

Observacao: ambientes corporativos devem utilizar variaveis de ambiente ou cofre de segredos para configuracoes sensiveis.

## 6. Aplicacao Principal

Arquivo: `api/main/main.py`

Responsabilidades:

- criar a aplicacao FastAPI;
- registrar os routers de usuarios, livros e enderecos.

Prefixos registrados:

- `/usuarios`
- `/livros`
- `/enderecos`

## 7. Configuracao de Banco de Dados

Arquivo: `api/database/conexao.py`

Responsabilidade:

- criar conexoes assincronas com o banco MySQL.

Variaveis de ambiente esperadas:

| Variavel | Descricao | Sensibilidade |
| --- | --- | --- |
| `MYSQL_HOST` | Host do banco de dados | Baixa |
| `MYSQL_PORT` | Porta do banco de dados | Baixa |
| `MYSQL_USER` | Usuario de conexao | Sensivel |
| `MYSQL_PASSWORD` | Senha de conexao | Sensivel |
| `MYSQL_DATABASE` | Nome do banco | Baixa |
| `JWT_SECRET_KEY` | Chave de assinatura dos tokens JWT | Sensivel |

Diretrizes:

- nao registrar valores reais dessas variaveis em documentos, prints, commits ou issues;
- nao versionar arquivos `.env` com credenciais reais;
- usar o arquivo `.env.example` apenas como referencia de configuracao;
- usar usuarios de banco com menor privilegio necessario;
- substituir credenciais padrao antes de qualquer ambiente compartilhado.

## 8. Banco de Dados

Arquivo: `api/database/biblioteca.sql`

O script cria o banco e as tabelas principais.

### Tabela `usuarios`

Campos principais:

- `id`
- `nome`
- `username`
- `email`
- `senha_hash`
- `criado_em`

Regras:

- `username` deve ser unico;
- `email` deve ser unico;
- a senha nao deve ser armazenada em texto puro;
- `senha_hash` nao deve ser retornado por rotas de listagem ou consulta.

### Tabela `generos`

Campos principais:

- `id`
- `nome`
- `disponivel`
- `criado_em`

Regras:

- `nome` deve ser unico;
- `disponivel` indica se o genero esta ativo para uso.

### Tabela `livros`

Campos principais:

- `id`
- `tipo`
- `data_publicacao`
- `preco`
- `criado_em`

Regras:

- `tipo` deve ser unico;
- `preco` nao pode ser negativo;
- `data_publicacao` nao pode estar no futuro.

### Tabela `enderecos`

Campos principais:

- `id`
- `logradouro`
- `numero`
- `bairro`
- `cidade`
- `estado`
- `cep`
- `criado_em`

Regras:

- `cep` deve possuir 8 digitos numericos;
- dados de endereco podem ser considerados dados pessoais conforme o contexto de uso e devem ser tratados com cuidado.

## 9. Seguranca e Autenticacao

Arquivo: `api/security/jwt_config.py`

Responsabilidades:

- configurar OAuth2;
- criar tokens JWT;
- validar tokens JWT em rotas protegidas.

Configuracoes relevantes:

- algoritmo JWT: `HS256`;
- tempo de expiracao do token: configurado na aplicacao;
- chave secreta: deve ser carregada pela variavel `JWT_SECRET_KEY` ou por cofre de segredos.

Diretrizes obrigatorias:

- nao documentar nem versionar a chave JWT real;
- nao expor tokens de acesso em logs, prints ou exemplos reais;
- rotacionar a chave caso ela tenha sido exposta;
- usar HTTPS em ambientes publicados;
- manter tokens com tempo de vida limitado.

Exemplo sanitizado de resposta de login:

```json
{
  "access_token": "<jwt_token>",
  "token_type": "bearer"
}
```

## 10. Models

Os models usam Pydantic e ficam em `api/models`.

### Usuario

Arquivo: `api/models/usuario_models.py`

Models principais:

- `LoginRequest`
- `Usuario`
- `UsuarioCreate`
- `UsuarioResponse`
- `UsuarioUpdate`

Regras:

- campos de senha existem apenas para entrada de dados;
- respostas de usuario nao devem retornar senha nem hash;
- senha deve obedecer ao tamanho minimo definido no model.

### Livro

Arquivo: `api/models/livro_models.py`

Models principais:

- `Livro`
- `GeneroRequest`

Regras:

- `data_publicacao` nao pode estar no futuro.

### Genero

Arquivo: `api/models/genero_models.py`

Model principal:

- `Genero`

Regras:

- remove espacos no inicio e no fim;
- normaliza o valor para minusculo.

### Endereco

Arquivo: `api/models/endereco_models.py`

Model principal:

- `Endereco`

Regras:

- aceita CEP com ou sem hifen;
- remove caracteres de formatacao;
- exige 8 digitos numericos.

### Autor

Arquivo: `api/models/autor_models.py`

Model principal:

- `Autor`

Observacao:

- ainda nao ha CRUD implementado para autores.

## 11. Service Principal

Arquivo: `api/services/biblioteca_service.py`

Classe principal:

```python
class BibliotecaService:
```

Responsabilidades:

- centralizar acesso ao banco;
- aplicar normalizacoes antes da persistencia;
- executar operacoes assincronas com `await`.

### Usuarios

Metodos:

- `gerar_hash_senha(senha: str)`
- `login(usuario, senha)`
- `cadastrar_usuario(usuario)`
- `listar_usuarios()`
- `buscar_usuario(usuario_id: int)`
- `atualizar_usuario(usuario_id: int, usuario)`
- `deletar_usuario(usuario_id: int)`

Pontos de seguranca:

- senhas sao transformadas em hash antes da persistencia;
- listagem e busca nao retornam `senha_hash`;
- conflitos de `username` ou `email` sao tratados pelo service.

### Generos

Metodos:

- `livros_disponiveis(livro)`
- `livros_indisponiveis(livro)`
- `adicionar_genero(genero)`

Observacao:

- apesar do nome `livros_disponiveis`, o metodo consulta a tabela `generos`.

### Livros

Metodos:

- `cadastro_livro(livro)`
- `listar_livros()`
- `buscar_livro(livro_id: int)`
- `atualizar_livro(livro_id: int, livro)`
- `deletar_livro(livro_id: int)`

Pontos importantes:

- `tipo` e normalizado no cadastro e na atualizacao;
- duplicidades sao tratadas no cadastro;
- busca e listagem retornam apenas os campos publicos do recurso.

### Enderecos

Metodos:

- `cadastrar_endereco(endereco)`
- `listar_enderecos()`
- `buscar_endereco(endereco_id: int)`
- `atualizar_endereco(endereco_id: int, endereco)`
- `deletar_endereco(endereco_id: int)`

Pontos importantes:

- `estado` e salvo em maiusculo;
- `cep` e validado pelo model;
- dados de endereco devem ser tratados como potencialmente sensiveis.

## 12. Endpoints

### Usuarios

Prefixo: `/usuarios`

| Metodo | Rota | Autenticacao | Descricao |
| --- | --- | --- | --- |
| `POST` | `/usuarios/login` | Publica | Autentica usuario e retorna JWT |
| `POST` | `/usuarios` | Publica | Cadastra usuario |
| `GET` | `/usuarios` | JWT | Lista usuarios |
| `GET` | `/usuarios/{usuario_id}` | JWT | Busca usuario por ID |
| `PUT` | `/usuarios/{usuario_id}` | JWT | Atualiza usuario |
| `DELETE` | `/usuarios/{usuario_id}` | JWT | Remove usuario |

Exemplo sanitizado de cadastro:

```json
{
  "nome": "Usuario Exemplo",
  "username": "usuario.exemplo",
  "email": "usuario.exemplo@dominio.local",
  "senha": "<senha-forte>"
}
```

### Livros e Generos

Prefixo: `/livros`

| Metodo | Rota | Autenticacao | Descricao |
| --- | --- | --- | --- |
| `GET` | `/livros/generos/disponiveis/{genero}` | Publica | Verifica disponibilidade de genero |
| `POST` | `/livros/generos` | JWT | Adiciona genero |
| `POST` | `/livros` | JWT | Cadastra livro |
| `GET` | `/livros` | Publica | Lista livros |
| `GET` | `/livros/{livro_id}` | Publica | Busca livro por ID |
| `PUT` | `/livros/{livro_id}` | JWT | Atualiza livro |
| `DELETE` | `/livros/{livro_id}` | JWT | Remove livro |

Exemplo sanitizado de livro:

```json
{
  "tipo": "romance",
  "data_publicacao": "2024-01-10",
  "preco": 49.9
}
```

### Enderecos

Prefixo: `/enderecos`

| Metodo | Rota | Autenticacao | Descricao |
| --- | --- | --- | --- |
| `POST` | `/enderecos` | JWT | Cadastra endereco |
| `GET` | `/enderecos` | Publica | Lista enderecos |
| `GET` | `/enderecos/{endereco_id}` | Publica | Busca endereco por ID |
| `PUT` | `/enderecos/{endereco_id}` | JWT | Atualiza endereco |
| `DELETE` | `/enderecos/{endereco_id}` | JWT | Remove endereco |

Exemplo sanitizado de endereco:

```json
{
  "logradouro": "Rua Exemplo",
  "numero": 100,
  "bairro": "Bairro Exemplo",
  "cidade": "Cidade Exemplo",
  "estado": "SP",
  "cep": "00000000"
}
```

## 13. Rotas Publicas e Protegidas

Rotas publicas:

- `POST /usuarios/login`
- `POST /usuarios`
- `GET /livros/generos/disponiveis/{genero}`
- `GET /livros`
- `GET /livros/{livro_id}`
- `GET /enderecos`
- `GET /enderecos/{endereco_id}`

Rotas protegidas por JWT:

- `GET /usuarios`
- `GET /usuarios/{usuario_id}`
- `PUT /usuarios/{usuario_id}`
- `DELETE /usuarios/{usuario_id}`
- `POST /livros/generos`
- `POST /livros`
- `PUT /livros/{livro_id}`
- `DELETE /livros/{livro_id}`
- `POST /enderecos`
- `PUT /enderecos/{endereco_id}`
- `DELETE /enderecos/{endereco_id}`

## 14. Uso no Swagger

1. Inicie a API.
2. Acesse `http://localhost:8000/docs`.
3. Cadastre um usuario de teste com dados ficticios.
4. Faca login em `POST /usuarios/login`.
5. Use o token retornado no botao `Authorize`.
6. Teste as rotas protegidas.

Formato do token:

```text
Bearer <jwt_token>
```

Nunca registrar tokens reais em documentacoes, mensagens, commits ou chamados.

## 15. Controles de Seguranca Recomendados

Antes de usar em ambiente compartilhado, homologacao ou producao:

- remover credenciais padrao do codigo e do SQL;
- carregar segredos por variaveis de ambiente ou cofre de segredos;
- revisar dados seed para garantir que nao contenham pessoas, e-mails ou senhas reais;
- nao commitar arquivos `.env`, dumps de banco ou colecoes com tokens preenchidos;
- substituir exemplos reais por placeholders;
- configurar logs para nao imprimir senhas, hashes, tokens ou payloads sensiveis;
- avaliar algoritmo de hash de senha mais adequado para producao, como bcrypt, Argon2 ou PBKDF2;
- aplicar HTTPS nos ambientes publicados;
- restringir CORS conforme os dominios autorizados;
- revisar permissoes do usuario de banco.

## 16. Observacoes Tecnicas

### Dados seed

O script SQL pode conter registros iniciais para facilitar testes locais. Esses registros devem usar apenas dados ficticios e senhas temporarias sem relacao com usuarios reais.

Em ambiente corporativo, recomenda-se:

- nao publicar credenciais seed reais;
- forcar troca de senha inicial quando aplicavel;
- remover usuarios seed antes de ambientes produtivos.

### Encoding

Algumas mensagens do projeto podem apresentar caracteres quebrados por divergencia de encoding. Recomenda-se padronizar os arquivos em UTF-8.

### CRUD de autores

Existe o model:

```text
api/models/autor_models.py
```

Ainda faltam:

- `api/routes/autor_routes.py`;
- metodos de autor em `BibliotecaService`;
- tabela `autores` no SQL.

## 17. Validacoes Recomendadas

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

## 18. Resumo Executivo dos Endpoints

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
