from flask import Blueprint, jsonify, request, render_template, url_for, redirect
from ..controllers.cliente_controller import ClienteController
from flask_login import login_required, current_user, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash

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
    dados = request.form.to_dict()
    # criptografa senha antes de salvar no banco de dados
    dados["senha"] = generate_password_hash(dados["senha"])
    # logica para cadastro do banco de dados
    try:
        cliente_controller.create(dados)
        flash("Cadastro realizado com sucesso! Faça login.", "success")
    except Exception as e:
        flash("Erro ao realizar cadastro. Email já pode estar em uso.", "danger")
    # redirecionar para tela de login
    return redirect(url_for("login_cadastro.login"))


@login_cadastro_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login_cadastro.login"))
