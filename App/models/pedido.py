from enum import Enum
from datetime import datetime
from . import db


class Status(Enum):
    CARRINHO: str = "CARRINHO"  # cliente ainda está escolhendo (este é o carrinho!)
    DISPONIVEL: str = "DISPONIVEL"  # Finalizado, aguardando a cozinha pegar
    FAZENDO: str = "FAZENDO"  # Cozinha está preparando
    FEITO: str = "FEITO"  # Pronto para entrega/retirada


class Pedido(db.Model):
    __tablename__ = "pedido"

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)

    # A data agora pode ser nula. Só preenchemos quando ele sair do status "CARRINHO"
    data = db.Column(db.DateTime, nullable=True)

    # O pedido nasce com o status de CARRINHO por padrão
    status = db.Column(db.String(20), default=Status.CARRINHO.value)

    # Relacionamento com o Cliente
    cliente = db.relationship("Cliente", back_populates="pedidos")

    # Um Pedido (que atua como carrinho inicialmente) tem vários Itens (ItemPedido)
    itens = db.relationship(
        "ItemPedido", backref="pedido", cascade="all, delete-orphan", lazy=True
    )

    def to_dict(self):
        lista_itens = [i.to_dict() for i in self.itens]
        return {
            "id": self.id,
            "cliente": self.cliente.nome if self.cliente else "N/A",
            "itens": lista_itens,
            "total_pedido": sum(item.get("subtotal", 0) for item in lista_itens),
            "status": self.status,
            # Se tiver data, formata bonitinho. Se não, avisa que está no carrinho.
            "data": (
                self.data.strftime("%d/%m/%Y %H:%M")
                if self.data
                else "Ainda no carrinho"
            ),
        }
