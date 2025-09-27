from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Bairro, AnoLancamento, QdeLancamento
from pydantic import BaseModel
from typing import List

app = FastAPI(title="API IPTU BH 2022")

# Modelos Pydantic para resposta
class BairroResponse(BaseModel):
    id: int
    nome: str
    
    class Config:
        from_attributes = True

class LancamentoResponse(BaseModel):
    bairro: str
    ano: int
    valor_total_lancado: float
    quantidade_lancamentos: int
    
    class Config:
        from_attributes = True

# Endpoints da API
@app.get("/")
def read_root():
    return {"message": "API IPTU Belo Horizonte 2022"}

@app.get("/bairros", response_model=List[BairroResponse])
def listar_bairros(db: Session = Depends(get_db)):
    """Lista todos os bairros"""
    bairros = db.query(Bairro).all()
    return bairros

@app.get("/lancamentos", response_model=List[LancamentoResponse])
def listar_lancamentos(db: Session = Depends(get_db)):
    """Lista todos os lançamentos de IPTU"""
    lancamentos = db.query(AnoLancamento).join(Bairro).join(QdeLancamento).all()
    
    resultado = []
    for lancamento in lancamentos:
        resultado.append({
            "bairro": lancamento.bairro.nome,
            "ano": lancamento.ano,
            "valor_total_lancado": lancamento.valor_total_lancado,
            "quantidade_lancamentos": lancamento.quantidades[0].quantidade_lancamento
        })
    
    return resultado

@app.get("/bairros/{bairro_id}", response_model=LancamentoResponse)
def obter_bairro(bairro_id: int, db: Session = Depends(get_db)):
    """Obtém informações de IPTU de um bairro específico"""
    lancamento = db.query(AnoLancamento).filter(
        AnoLancamento.bairro_id == bairro_id
    ).first()
    
    if not lancamento:
        raise HTTPException(status_code=404, detail="Bairro não encontrado")
    
    return {
        "bairro": lancamento.bairro.nome,
        "ano": lancamento.ano,
        "valor_total_lancado": lancamento.valor_total_lancado,
        "quantidade_lancamentos": lancamento.quantidades[0].quantidade_lancamento
    }

@app.get("/buscar/{nome_bairro}", response_model=LancamentoResponse)
def buscar_por_nome(nome_bairro: str, db: Session = Depends(get_db)):
    """Busca lançamentos por nome do bairro"""
    bairro = db.query(Bairro).filter(Bairro.nome.ilike(f"%{nome_bairro}%")).first()
    
    if not bairro:
        raise HTTPException(status_code=404, detail="Bairro não encontrado")
    
    lancamento = db.query(AnoLancamento).filter(
        AnoLancamento.bairro_id == bairro.id
    ).first()
    
    return {
        "bairro": bairro.nome,
        "ano": lancamento.ano,
        "valor_total_lancado": lancamento.valor_total_lancado,
        "quantidade_lancamentos": lancamento.quantidades[0].quantidade_lancamento
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)