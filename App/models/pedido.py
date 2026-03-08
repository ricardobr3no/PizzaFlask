from enum import Enum
from datetime import datetime

from . import db


class Status(Enum):
    DISPONIVEL: str = "DISPONIVEL"
    FAZENDO: str = "FAZENDO"
    FEITO: str = "FEITO"


class Pedido(db.Model):
    __tablename__ = "pedido"
    # columns
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=datetime.now())
    status = db.Column(db.String(20), default=Status.DISPONIVEL.value)

    # Um pedido tem vários itens através da tabela ItemPedido
    cliente = db.relationship("Cliente", back_populates="pedidos")
    itens = db.relationship(
        "ItemPedido", back_populates="pedido", cascade="all, delete-orphan"
    )

    def to_dict(self):
        lista_itens = [i.to_dict() for i in self.itens]
        return {
            "id": self.id,
            "cliente": self.cliente.nome if self.cliente else "N/A",
            "itens": lista_itens,
            "total_pedido": sum(item["subtotal"] for item in lista_itens),
            "status": self.status,
        }
