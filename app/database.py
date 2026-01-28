from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# INSTÂNCIA A CLASSE DO GERENCIADOR DE DB
db = SQLAlchemy(model_class=Base)
