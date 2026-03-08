from . import db


class ItemPedido(db.Model):
    __tablename__ = "item_pedido"

    id = db.Column(db.Integer, primary_key=True)

    # Chave estrangeira ligando este item ao Pedido/Carrinho
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedido.id"), nullable=False)

    # Chave estrangeira ligando este item ao Item (Lanche/Bebida)
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"), nullable=False)

    quantidade = db.Column(db.Integer, nullable=False, default=1)
    subtotal = db.Column(db.Float, nullable=False)

    # Para pegar facilmente o nome do lanche depois
    item = db.relationship("Item")

    def to_dict(self):
        return {
            "id": self.id,
            "produto_nome": self.item.nome if self.item else "Desconhecido",
            "quantidade": self.quantidade,
            "subtotal": self.subtotal,
        }
