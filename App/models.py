from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base  

class Bairro(Base):
    __tablename__ = "bairros"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    anos = relationship("AnoLancamento", back_populates="bairro")

class AnoLancamento(Base):
    __tablename__ = "anos_lancamento"

    id = Column(Integer, primary_key=True, index=True)
    ano = Column(Integer, index=True)
    valor_total_lancado = Column(Float)
    bairro_id = Column(Integer, ForeignKey("bairros.id"))
    bairro = relationship("Bairro", back_populates="anos")
    quantidades = relationship("QdeLancamento", back_populates="ano_lancamento")

class QdeLancamento(Base):
    __tablename__ = "qtdes_lancamento"

    id = Column(Integer, primary_key=True, index=True)
    quantidade_lancamento = Column(Integer)
    ano_lancamento_id = Column(Integer, ForeignKey("anos_lancamento.id"))
    ano_lancamento = relationship("AnoLancamento", back_populates="quantidades")