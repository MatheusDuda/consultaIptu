from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base  # ← Mude esta linha
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./iptu_2022.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()  # ← Agora sem warning

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()