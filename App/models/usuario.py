from enum import Enum
from flask_login import UserMixin
from . import db


class Role(Enum):
    CLIENTE = "CLIENTE"
    ADMIN = "ADMIN"
    # COZINHA = "COZINHA" <- Exemplo de como seria fácil expandir no futuro


class Usuario(db.Model, UserMixin):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(40), nullable=False)

    # Define o que esse usuário é. Por padrão, quem se cadastra é CLIENTE.
    role = db.Column(db.String(20), default=Role.CLIENTE.value)

    # Um usuário (se for cliente) pode ter vários pedidos
    pedidos = db.relationship(
        "Pedido", back_populates="usuario", cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "role": self.role,
            "total_pedidos": len(self.pedidos),
        }
