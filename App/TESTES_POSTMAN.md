# Testes da API IPTU BH 2022 - Coleção Postman

## Pré-requisitos
- API rodando em http://127.0.0.1:8000
- Postman instalado ou usar a interface web

## Como importar a coleção

### Opção 1: Postman Web
1. Acesse https://web.postman.co
2. Clique em "Import" 
3. Selecione o arquivo `postman_collection.json`
4. Clique em "Import"

### Opção 2: Postman Desktop
1. Abra o Postman
2. File → Import
3. Selecione o arquivo `postman_collection.json`

## Endpoints para testar

### 1. Health Check (`GET /`)
- **URL:** http://127.0.0.1:8000/
- **Descrição:** Verifica se a API está online
- **Status esperado:** 200 OK

### 2. Listar Bairros (`GET /bairros`)
- **URL:** http://127.0.0.1:8000/bairros
- **Descrição:** Retorna lista de todos os bairros
- **Status esperado:** 200 OK
- **Resposta:** Array com 451 bairros

### 3. Listar Lançamentos (`GET /lancamentos`)
- **URL:** http://127.0.0.1:8000/lancamentos
- **Descrição:** Retorna todos os lançamentos de IPTU
- **Status esperado:** 200 OK
- **Resposta:** Array com dados completos

### 4. Buscar por ID (`GET /bairros/{id}`)
- **URL:** http://127.0.0.1:8000/bairros/1
- **Descrição:** Busca dados de um bairro específico por ID
- **Status esperado:** 200 OK

### 5. Buscar por Nome (`GET /buscar/{nome}`)
- **URL:** http://127.0.0.1:8000/buscar/savassi
- **Descrição:** Busca bairros por nome (case insensitive)
- **Status esperado:** 200 OK

### 6. Teste de Erro (`GET /bairros/9999`)
- **URL:** http://127.0.0.1:8000/bairros/9999
- **Descrição:** Testa tratamento de erro para ID inexistente
- **Status esperado:** 404 Not Found

## Resultados Esperados

Cada teste deve retornar:
- **Status HTTP correto**
- **JSON válido** no corpo da resposta
- **Dados consistentes** com o banco de dados

## Evidências de Teste
- Print das respostas de cada endpoint
- Confirmação dos status HTTP
- Verificação da estrutura dos JSON retornados