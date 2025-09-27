from pydantic import BaseModel
from typing import List, Optional

# -------- QDE LANCAMENTO --------
class QdeLancamentoBase(BaseModel):
    quantidade_lancamento: int

class QdeLancamentoCreate(QdeLancamentoBase):
    pass

class QdeLancamento(QdeLancamentoBase):
    id: int
    class Config:
        orm_mode = True

# -------- ANO LANCAMENTO --------
class AnoLancamentoBase(BaseModel):
    ano: int
    valor_total_lancado: float

class AnoLancamentoCreate(AnoLancamentoBase):
    bairro_id: int
    qtdes: Optional[List[QdeLancamentoCreate]] = []

class AnoLancamento(AnoLancamentoBase):
    id: int
    bairro_id: int
    quantidades: List[QdeLancamento] = []
    class Config:
        orm_mode = True

# -------- BAIRRO --------
class BairroBase(BaseModel):
    nome: str

class BairroCreate(BairroBase):
    pass

class Bairro(BairroBase):
    id: int
    anos: List[AnoLancamento] = []
    class Config:
        orm_mode = True
