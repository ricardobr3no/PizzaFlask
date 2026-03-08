from . import db


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
