from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
from models import Bairro, AnoLancamento, QdeLancamento
from importar_iptu_csv import importar_iptu
import os
import time
import json

def banco_ja_existe():
    """Verifica se o banco ja tem dados"""
    db = SessionLocal()
    try:
        # Verifica se ja existem bairros no banco
        total_bairros = db.query(Bairro).count()
        return total_bairros > 0
    finally:
        db.close()

def criar_banco_dados():
    """Cria o banco de dados e importa os dados do IPTU"""
    print("=" * 60)
    print("CRIANDO BANCO DE DADOS E IMPORTANDO IPTU")
    print("=" * 60)
    
    # Verifica se o banco ja existe
    if banco_ja_existe():
        print("AVISO: Banco de dados ja existe com dados!")
        print("Deseja sobrescrever os dados existentes?")
        resposta = input("Digite 'SIM' para sobrescrever ou 'NAO' para usar dados existentes: ").strip().upper()
        
        if resposta != "SIM":
            print("Usando banco de dados existente.")
            return True
    
    # Verifica se o arquivo CSV existe
    if not os.path.exists("iptu-bairro.csv"):
        print("ERRO: Arquivo iptu-bairro.csv nao encontrado")
        print("Certifique-se de que o arquivo esta na mesma pasta")
        return False
    
    print("Arquivo iptu-bairro.csv encontrado")
    
    # Cria todas as tabelas no banco (se nao existirem)
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas/verificadas com sucesso")
    
    # Cria uma sessao do banco
    db = SessionLocal()
    
    try:
        # Importa dados para o ano 2022
        importar_iptu(db, 2022)
        
        # Verifica os dados importados
        total_bairros = db.query(Bairro).count()
        total_anos = db.query(AnoLancamento).count()
        total_qdes = db.query(QdeLancamento).count()
        
        print("\nESTATISTICAS DA IMPORTACAO:")
        print(f"   Bairros: {total_bairros}")
        print(f"   Anos de lancamento: {total_anos}")
        print(f"   Quantidades de lancamento: {total_qdes}")
        
        return True
        
    except Exception as e:
        print(f"ERRO na importacao: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def estatisticas_banco():
    """Mostra estatisticas do banco atual"""
    db = SessionLocal()
    try:
        total_bairros = db.query(Bairro).count()
        total_anos = db.query(AnoLancamento).count()
        total_qdes = db.query(QdeLancamento).count()
        
        print("\nESTATISTICAS DO BANCO ATUAL:")
        print(f"   Bairros: {total_bairros}")
        print(f"   Anos de lancamento: {total_anos}")
        print(f"   Quantidades de lancamento: {total_qdes}")
        
    finally:
        db.close()

def executar_analise_exploratoria():
    """Executa a analise exploratoria dos dados"""
    print("\n" + "=" * 60)
    print("EXECUTANDO ANALISE EXPLORATORIA")
    print("=" * 60)
    
    try:
        from analise_exploratoria import analise_exploratoria
        analise_exploratoria()
        return True
    except Exception as e:
        print(f"ERRO na analise exploratoria: {e}")
        return False

def executar_api():
    """Inicia a API FastAPI"""
    print("\n" + "=" * 60)
    print("INICIANDO API FASTAPI")
    print("=" * 60)
    print("API rodando em: http://127.0.0.1:8000")
    print("Documentacao: http://127.0.0.1:8000/docs")
    print("Pressione CTRL+C para parar o servidor")
    print("=" * 60)
    
    try:
        from api import app
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    except KeyboardInterrupt:
        print("\nServidor parado pelo usuario")
    except Exception as e:
        print(f"ERRO na API: {e}")

def exportar_colecao_postman():
    """Exporta a colecao do Postman para testes da API"""
    print("\n" + "=" * 60)
    print("EXPORTANDO COLECAO POSTMAN")
    print("=" * 60)
    
    colecao = {
        "info": {
            "name": "API IPTU BH 2022",
            "description": "API para consulta de dados do IPTU de Belo Horizonte - Exercicio 2022",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": [
            {
                "name": "Health Check",
                "request": {
                    "method": "GET",
                    "header": [],
                    "url": {
                        "raw": "http://127.0.0.1:8000/",
                        "protocol": "http",
                        "host": ["127", "0", "0", "1"],
                        "port": "8000",
                        "path": [""]
                    },
                    "description": "Verifica se a API esta online"
                }
            },
            {
                "name": "Listar Todos os Bairros",
                "request": {
                    "method": "GET",
                    "header": [],
                    "url": {
                        "raw": "http://127.0.0.1:8000/bairros",
                        "protocol": "http",
                        "host": ["127", "0", "0", "1"],
                        "port": "8000",
                        "path": ["bairros"]
                    },
                    "description": "Retorna lista de todos os bairros"
                }
            },
            {
                "name": "Listar Todos os Lancamentos",
                "request": {
                    "method": "GET",
                    "header": [],
                    "url": {
                        "raw": "http://127.0.0.1:8000/lancamentos",
                        "protocol": "http",
                        "host": ["127", "0", "0", "1"],
                        "port": "8000",
                        "path": ["lancamentos"]
                    },
                    "description": "Retorna todos os lancamentos de IPTU"
                }
            },
            {
                "name": "Buscar Bairro por ID",
                "request": {
                    "method": "GET",
                    "header": [],
                    "url": {
                        "raw": "http://127.0.0.1:8000/bairros/1",
                        "protocol": "http",
                        "host": ["127", "0", "0", "1"],
                        "port": "8000",
                        "path": ["bairros", "1"]
                    },
                    "description": "Busca dados de um bairro especifico por ID"
                }
            },
            {
                "name": "Buscar Bairro por Nome",
                "request": {
                    "method": "GET",
                    "header": [],
                    "url": {
                        "raw": "http://127.0.0.1:8000/buscar/savassi",
                        "protocol": "http",
                        "host": ["127", "0", "0", "1"],
                        "port": "8000",
                        "path": ["buscar", "savassi"]
                    },
                    "description": "Busca bairros por nome (case insensitive)"
                }
            },
            {
                "name": "Buscar Bairro Inexistente",
                "request": {
                    "method": "GET",
                    "header": [],
                    "url": {
                        "raw": "http://127.0.0.1:8000/bairros/9999",
                        "protocol": "http",
                        "host": ["127", "0", "0", "1"],
                        "port": "8000",
                        "path": ["bairros", "9999"]
                    },
                    "description": "Testa tratamento de erro para ID inexistente"
                }
            }
        ]
    }
    
    try:
        with open('postman_collection.json', 'w', encoding='utf-8') as f:
            json.dump(colecao, f, indent=2, ensure_ascii=False)
        
        print("Colecao Postman exportada com sucesso!")
        print("Arquivo: postman_collection.json")
        print("\nINSTRUCOES:")
        print("1. Acesse https://web.postman.co")
        print("2. Clique em 'Import'")
        print("3. Selecione o arquivo postman_collection.json")
        print("4. Clique em 'Import'")
        print("5. Execute os testes com a API rodando")
        
    except Exception as e:
        print(f"ERRO ao exportar colecao: {e}")

def menu_principal():
    """Menu interativo para o usuario"""
    while True:
        print("\n" + "=" * 60)
        print("SISTEMA IPTU BELO HORIZONTE 2022")
        print("=" * 60)
        
        # Mostra status do banco
        if banco_ja_existe():
            print("STATUS: Banco de dados EXISTE com dados")
            estatisticas_banco()
        else:
            print("STATUS: Banco de dados VAZIO ou NAO EXISTE")
        
        print("\nOPCOES:")
        print("1 - Executar tudo (Banco + Analise + API)")
        print("2 - Apenas criar/recriar banco de dados")
        print("3 - Apenas analise exploratoria") 
        print("4 - Apenas executar API")
        print("5 - Ver estatisticas do banco")
        print("6 - Exportar colecao Postman")
        print("7 - Sair")
        print("=" * 60)
        
        opcao = input("Escolha uma opcao (1-7): ").strip()
        
        if opcao == "1":
            # Executa tudo
            if criar_banco_dados() or banco_ja_existe():
                time.sleep(1)
                if executar_analise_exploratoria():
                    time.sleep(1)
                    executar_api()
                    
        elif opcao == "2":
            criar_banco_dados()
            
        elif opcao == "3":
            executar_analise_exploratoria()
            
        elif opcao == "4":
            if not banco_ja_existe():
                print("AVISO: Banco vazio. Execute a opcao 1 ou 2 primeiro.")
            else:
                executar_api()
            
        elif opcao == "5":
            if banco_ja_existe():
                estatisticas_banco()
            else:
                print("Banco de dados vazio ou nao existe.")
                
        elif opcao == "6":
            exportar_colecao_postman()
                
        elif opcao == "7":
            print("Saindo...")
            break
            
        else:
            print("Opcao invalida! Tente novamente.")

if __name__ == "__main__":
    # Verifica se existem os arquivos necessarios
    arquivos_necessarios = ["iptu-bairro.csv", "api.py", "analise_exploratoria.py"]
    
    print("VERIFICANDO ARQUIVOS NECESSARIOS:")
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"   OK - {arquivo}")
        else:
            print(f"   FALTANDO - {arquivo}")
    
    # Executa o menu principal
    menu_principal()