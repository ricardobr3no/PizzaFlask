import logging
import os

from dotenv import load_dotenv
from sqlalchemy import text
from flask import Blueprint, Flask, render_template, request
from flask_cors import CORS

from .models import db

from .routes.login_cadastro_routes import login_cadastro_bp
from .routes.home_routes import home_bp


class App:
    def __init__(self, force=False) -> None:
        # criar app
        self.app = Flask(__name__)
        # configuracoes
        self._configurar_database(force)
        # rotas da aplicacao
        self._configurar_rotas_bp(login_cadastro_bp, home_bp, url_prefix="")

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
                # apaga todas as tabelas
                logging.warning("Resetando as tabelas (force=True)...")
                db.drop_all()
                db.session.commit()

            db.create_all()
            db.session.commit()

    def _configurar_rotas_bp(self, *rotas_bp: Blueprint, url_prefix=""):
        # adiciona blueprint das rotas
        for rota_bp in rotas_bp:
            self.app.register_blueprint(rota_bp, url_prefix=url_prefix)

    def run(self, port=None, debug=True):
        self.app.run(port=5000 if not port else port, debug=debug)


if __name__ == "__main__":
    load_dotenv()
    app = App(force=False)
    app.run()
