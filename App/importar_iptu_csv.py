import pandas as pd
from sqlalchemy.orm import Session
from models import Bairro, AnoLancamento, QdeLancamento

def importar_iptu(db: Session, ano: int):
    try:
        # Usa o arquivo local
        df = pd.read_csv("iptu-bairro.csv", sep=";", encoding="utf-8")
        print(f"Dataset carregado: {len(df)} registros")
        
        # Verifica colunas necessarias
        colunas_necessarias = ["BAIRRO", "VALOR_TOTAL_LANCADO", "QDE_LANCAMENTOS"]
        for coluna in colunas_necessarias:
            if coluna not in df.columns:
                raise ValueError(f"Coluna '{coluna}' nao encontrada no dataset")

        total_registros = 0
        for index, row in df.iterrows():
            # Limpa e valida dados
            bairro_nome = str(row["BAIRRO"]).strip()
            if not bairro_nome or bairro_nome == "nan":
                continue

            # Converte valores brasileiros para float
            valor_str = str(row["VALOR_TOTAL_LANCADO"]).replace(".", "").replace(",", ".")
            quantidade_str = str(row["QDE_LANCAMENTOS"]).replace(".", "")

            # Verifica se o bairro ja existe
            bairro = db.query(Bairro).filter(Bairro.nome == bairro_nome).first()
            if not bairro:
                bairro = Bairro(nome=bairro_nome)
                db.add(bairro)
                db.commit()
                db.refresh(bairro)
                print(f"Novo bairro adicionado: {bairro.nome}")

            # Cria o lancamento do ano
            ano_lancamento = AnoLancamento(
                ano=ano,
                valor_total_lancado=float(valor_str),
                bairro_id=bairro.id
            )
            db.add(ano_lancamento)
            db.commit()
            db.refresh(ano_lancamento)

            # Cria a quantidade de lancamentos
            qde = QdeLancamento(
                quantidade_lancamento=int(float(quantidade_str)),  # Converte para int
                ano_lancamento_id=ano_lancamento.id
            )
            db.add(qde)
            db.commit()

            total_registros += 1
            if total_registros % 10 == 0:
                print(f"Processando: {total_registros} bairros...")

        print(f"Importacao concluida para o ano {ano}")
        print(f"Total de bairros processados: {total_registros}")
        
    except Exception as e:
        db.rollback()
        print(f"Erro durante a importacao: {e}")
        raise