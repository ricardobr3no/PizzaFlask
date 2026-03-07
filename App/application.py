import logging
import os

from dotenv import load_dotenv
from flask import Blueprint, Flask, render_template, request
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
        self._configurar_database(force=False)
        self._configurar_rotas_bp(clientes_bp, pedidos_bp, itens_bp, url_prefix="/api")
        self._configurar_rotas_frontend()
        
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

    def _configurar_rotas_bp(self, *rotas_bp: Blueprint, url_prefix=""):
        # rota inicial
        @self.app.route(url_prefix, methods=["GET"])
        def home_api():
            return "Welcome to the Pizza Flask API!"
        # adiciona blueprint das rotas
        for rota_bp in rotas_bp:
            self.app.register_blueprint(rota_bp, url_prefix=url_prefix)
            
    
    def _configurar_rotas_frontend(self):
        # rota inicial
        @self.app.route("/login", methods=["GET"])
        def index():
            return render_template("login.html")
            
        @self.app.route("/login", methods=["POST"])
        def login():
            # pegar dados do formulario
            nome = request.form.get("nome")
            email = request.form.get("email")
            # logica de verificacao do banco de dados
            return "Login realizado com sucesso!"
            
        @self.app.route("/cadastro", methods=["POST"])
        def cadastro():
            # pegar dados do formulario
            nome = request.form.get("nome")
            email = request.form.get("email")
            # logica para cadastro do banco de dados
            return "Cadastro realizado com sucesso!"

    def run(self, port=None, debug=True):
        self.app.run(port=5000 if not port else port, debug=debug)


if __name__ == "__main__":
    load_dotenv()
    app = Application()
    app.run()
