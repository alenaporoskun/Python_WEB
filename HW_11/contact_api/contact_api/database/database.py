from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL для підключення до бази даних PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:567234@localhost:5432/db_postgres1"

# Створення об'єкту рушія (engine)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Створення сеансу (session) для роботи з базою даних
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
Base.metadata.create_all(bind=engine)

# Функція для отримання сеансу бази даних
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
