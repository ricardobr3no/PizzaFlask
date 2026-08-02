from flask import Blueprint, jsonify, request, render_template, url_for, redirect, flash
from flask_login import login_required, current_user, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash

from ..controllers import UserController
from ..models.usuario import Role

# criamos blueprint para login
login_cadastro_bp = Blueprint("login_cadastro", __name__)
# Instancia o controller genérico para Client
user_controller = UserController()


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
        # logica de verificacao do banco de dados (procura usuario pelo email)
        user_encontrado = user_controller.query({"email": email})
        if user_encontrado:
            print("user:", user_encontrado.to_dict())

        # redirecionar para tela do sistema
        if user_encontrado and check_password_hash(user_encontrado.senha, senha):
            login_user(user_encontrado)  # entrar com esse usuario
            if user_encontrado.role == Role.CLIENTE.value:
                return redirect(url_for("home.home"))
            elif user_encontrado.role == Role.ADMIN.value:
                return redirect(url_for("admin.dashboard"))
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
        user_controller.create(dados)
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
