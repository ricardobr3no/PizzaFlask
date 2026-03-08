from . import db


class Cliente(db.Model):
    __tablename__ = "cliente"
    # columns
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(40), nullable=False)

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
