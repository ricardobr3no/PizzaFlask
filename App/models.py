from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Cliente(db.Model):
    __tablename__ = "cliente"
    # columns
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Um cliente pode ter vários pedidos
    pedidos = db.relationship(
        "Pedido", back_populates="cliente", cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "total_pedidos": len(self.pedidos),
        }


class Item(db.Model):
    __tablename__ = "item"
    # columns
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False, unique=True)
    preco = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    imagem = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "preco": self.preco}


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


class Pedido(db.Model):
    __tablename__ = "pedido"
    # columns
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=datetime.now())

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
        }
