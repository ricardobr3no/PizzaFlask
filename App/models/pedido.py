from enum import Enum
from datetime import datetime
from . import db


class Status(Enum):
    CARRINHO: str = "CARRINHO"
    DISPONIVEL: str = "DISPONIVEL"
    FAZENDO: str = "FAZENDO"
    FEITO: str = "FEITO"


class Pedido(db.Model):
    __tablename__ = "pedido"

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    data = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default=Status.CARRINHO.value)

    usuario = db.relationship("Usuario", back_populates="pedidos")

    itens = db.relationship(
        "ItemPedido", backref="pedido", cascade="all, delete-orphan", lazy=True
    )

    def to_dict(self):
        lista_itens = [i.to_dict() for i in self.itens]
        return {
            "id": self.id,
            "usuario": self.usuario.nome if self.usuario else "N/A",
            "itens": lista_itens,
            "total_pedido": sum(item.get("subtotal", 0) for item in lista_itens),
            "status": self.status,
            "data": (
                self.data.strftime("%d/%m/%Y %H:%M")
                if self.data
                else "Ainda no carrinho"
            ),
        }
