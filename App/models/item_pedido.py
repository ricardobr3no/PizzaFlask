from . import db


class ItemPedido(db.Model):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    __tablename__ = "item_pedido"
    # columns
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedido.id"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)

    # Relacionamentos para facilitar o acesso
    item = db.relationship("Item")
    pedido = db.relationship("Pedido", back_populates="itens")

    def to_dict(self):
        return {
            "item_id": self.item_id,
            "nome": self.item.nome if self.item else None,
            "preco_unitario": self.item.preco if self.item else 0,
            "quantidade": self.quantidade,
            "subtotal": (self.item.preco * self.quantidade) if self.item else 0,
        }
