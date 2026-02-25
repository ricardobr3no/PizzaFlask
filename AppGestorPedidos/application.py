import logging
import os

from dotenv import load_dotenv
from flask import Flask
from flask.sansio.blueprints import Blueprint
from flask_cors import CORS

from .models import db
from .routes.cliente_routes import clientes_bp
from .routes.item_routes import itens_bp
from .routes.pedido_routes import pedidos_bp


class Application:
    def __init__(self) -> None:
        # criar app
        self.app = Flask(__name__)
        # configuracoes
        self._configurar_database(force=True)
        self.configurar_rotas_bp(clientes_bp, pedidos_bp, itens_bp, url_prefix="")
        # cofigurar cors
        CORS(self.app)

    def _configurar_database(self, force: bool):
        # Configura o banco de dados SQLite
        self.app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
        # Inicializa o app com a extensão do banco
        db.init_app(self.app)

        # Cria as tabelas antes da primeira requisição
        with self.app.app_context():
            if force:
                logging.warning("Resetando as tabelas (force=True)...")
                db.drop_all()
                db.session.commit()

            db.create_all()
            db.session.commit()

    def configurar_rotas_bp(self, *rotas_bp: Blueprint, url_prefix=""):
        # adiciona blueprint das rotas
        for rota_bp in rotas_bp:
            self.app.register_blueprint(rota_bp, url_prefix=url_prefix)

    def run(self, port=None, debug=True):
        self.app.run(port=5000 if not port else port, debug=debug)


if __name__ == "__main__":
    load_dotenv()
    app = Application()
    app.run()
