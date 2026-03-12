import logging
import os

from functools import wraps


from dotenv import load_dotenv

from sqlalchemy import text

from flask import (
    Blueprint,
    Flask,
    render_template,
    request,
    send_from_directory,
)

from flask_cors import CORS

from flask_login import LoginManager, current_user

from .models import db
from .controllers import UserController
from .routes import login_cadastro_bp, home_bp, admin_bp

login_manager = LoginManager()
cliente_ctrl = UserController()


@login_manager.user_loader
def load_user(user_id: id):
    # Esta função diz ao Flask-Login como procurar um utilizador na base de dados pelo seu ID
    return cliente_ctrl.get_by_id(user_id)


class App:

    def __init__(self, force=False) -> None:

        # criar app
        self.app = Flask(__name__)
        # Adicione uma chave secreta para as sessões funcionarem (segurança)
        self.app.secret_key = os.getenv("SECRET_KEY", "super_senha_secreta_123")

        # configuracoes
        self._configurar_database(force)
        # rotas da aplicacao principa (Home e Login ficam na raiz)
        self._configurar_rotas_bp(login_cadastro_bp, home_bp, url_prefix="")
        # rota do administrador (Forçamos o prefixo correto aqui)
        self._configurar_rotas_bp(admin_bp, url_prefix="/admin")
        # cofigurar cors
        CORS(self.app)

        # inicializar login_manager
        login_manager.init_app(self.app)
        # Configurar para onde redirecionar utilizadores não autenticados
        # O nome é 'nome_do_blueprint.nome_da_funcao'
        login_manager.login_view = "login_cadastro.login"
        login_manager.login_message = (
            "Por favor, inicie sessão para aceder a esta página."
        )
        login_manager.login_message_category = "warning"

        # configurar favicon
        @self.app.route("/favicon.ico")
        def favicon():

            return send_from_directory(
                os.path.join(self.app.root_path, "static", "images"),
                "icons8-pizza-32.png",
                mimetype="image/png",
            )

    def _configurar_database(self, force: bool):

        # Configura o banco de dados SQLite

        self.app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
            "DATABASE_URI", "sqlite:///project.db"
        )

        # Inicializa o app com a extensão do banco
        db.init_app(self.app)

        # Cria as tabelas antes da primeira requisição

        with self.app.app_context():

            if force:

                # apaga todas as tabelas

                logging.warning("Resetando as tabelas (force=True)...")
                db.drop_all()
                db.session.commit()

            # criar tabelas

            logging.warning("Criando tabelas...")
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
