from abc import ABC
from flask import abort
from flask_sqlalchemy import SQLAlchemy

from ..models import db


class BaseController(ABC):
    def __init__(self, model):
        self.model: db.Model = model
        self.db: SQLAlchemy = db

    def get_all(self) -> list:
        """Retorna todos os registros do modelo."""
        return self.model.query.all()

    def get_by_id(self, record_id: int):
        """Retorna um registro específico pelo ID ou lança erro 404."""
        record = self.model.query.get(record_id)
        if not record:
            abort(404, description=f"{self.model.__name__} não encontrado.")
        return record

    def query(self, filters: dict):
        """
        Busca registros baseados em campos dinâmicos.
        Ex: buscar(email="joao@pizzaria.com") ou buscar(nome="Margherita")
        """
        # Filtra o dicionário: mantém apenas o que é coluna no banco
        valid_filters = {k: v for k, v in filters.items() if hasattr(self.model, k)}
        # O filter_by aceita o desempacotamento de dicionário (**)
        return self.model.query.filter_by(**valid_filters).first()

    def query_all(self, filters: dict) -> list:
        """Retorna uma lista de todos os registros que coincidem com o filtro."""
        # Filtra o dicionário: mantém apenas o que é coluna no banco
        valid_filters = {k: v for k, v in filters.items() if hasattr(self.model, k)}
        # O filter_by aceita o desempacotamento de dicionário (**)
        return self.model.query.filter_by(**valid_filters).all()

    def create(self, data: dict):
        """Cria um novo registro no banco de dados."""
        try:
            new_record = self.model(**data)
            self.db.session.add(new_record)
            self.db.session.commit()
            return new_record
        except Exception as e:
            self.db.session.rollback()
            abort(400, description=f"Erro ao criar registro: {str(e)}")

    def update(self, record_id: int, data: dict):
        """Atualiza um registro existente."""
        record = self.get_by_id(record_id)
        try:
            for key, value in data.items():
                if hasattr(record, key):
                    setattr(record, key, value)
            self.db.session.commit()
            return record
        except Exception as e:
            self.db.session.rollback()
            abort(400, description=f"Erro ao atualizar registro: {str(e)}")

    def delete(self, record_id: int):
        """Deleta um registro existente."""
        record = self.get_by_id(record_id)
        try:
            self.db.session.delete(record)
            self.db.session.commit()
            return True
        except Exception as e:
            self.db.session.rollback()
            abort(400, description=f"Erro ao deletar registro: {str(e)}")
