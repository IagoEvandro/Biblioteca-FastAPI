# Biblioteca FastAPI

API REST para gerenciamento de biblioteca, desenvolvida com FastAPI, MySQL e autenticacao JWT.

## Documentacao

A documentacao tecnica completa esta em:

```text
docs/projeto_biblioteca_api.md
```

## Configuracao Segura

Use `.env.example` como referencia e configure as variaveis reais apenas no arquivo `.env` local ou em um cofre de segredos.

Nao versionar:

- senhas;
- tokens;
- chaves JWT;
- dumps de banco;
- dados pessoais reais.

## Execucao Local

```powershell
.\.venv\Scripts\python.exe -m uvicorn api.main.main:app --reload
```

Documentacao interativa:

```text
http://localhost:8000/docs
```
