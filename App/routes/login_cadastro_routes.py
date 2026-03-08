from flask import Blueprint, jsonify, request, render_template, url_for, redirect
from ..controllers.cliente_controller import ClienteController

# criamos blueprint para login
login_cadastro_bp = Blueprint("login_cadastro", __name__)
# Instancia o controller genérico para Client
cliente_controller = ClienteController()


# rota inicial
@login_cadastro_bp.route("/login", methods=["GET", "POST"])
def login():
    print(request.form.to_dict())

    if request.method == "GET":
        return render_template("login.html")

    elif request.method == "POST":
        # pegar dados do formulario
        email = request.form.get("email")
        senha = request.form.get("senha")
        # logica de verificacao do banco de dados
        cliente_encontrado = cliente_controller.query(request.form.to_dict())

        # redirecionar para tela do sistema
        if cliente_encontrado:
            return redirect(url_for("home.home"))
        else:
            # recarregar e mostrar mensagem de erro
            return render_template(
                "login.html",
                erro="Email ou senha incorretos!",
                email=email,
                senha=senha,
            )


@login_cadastro_bp.route("/cadastro", methods=["POST"])
def cadastro():
    # pegar dados do formulario
    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")
    # logica para cadastro do banco de dados
    novo_registro = cliente_controller.create(request.form.to_dict())
    print(request.form.to_dict())
    # redirecionar para tela de login (talvez adicionar notificação)
    return redirect(url_for("login_cadastro.login"))
