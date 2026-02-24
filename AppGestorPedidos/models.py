from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Cliente(db.Model):
    __tablename__ = "cliente"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # CORRIGIDO: Agora aponta para a classe 'ItemCliente'
    pedidos = db.relationship("ItemCliente", backref="cliente", lazy=True)

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "email": self.email}


class Item(db.Model):
    __tablename__ = "item"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False, unique=True)
    preco = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "preco": self.preco}


class ItemCliente(db.Model):
    __tablename__ = "item_cliente"
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

    # ADICIONADO: Permite acessar dados do item via pedido (ex: pedido.item.name)
    item = db.relationship("Item")

    def to_dict(self):
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "item_id": self.item_id,
            "nome_item": self.item.nome if self.item else None,  # Útil para o front-end
            "quantidade": self.quantidade,
        }
