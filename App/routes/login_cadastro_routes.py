from flask import Blueprint, jsonify, request, render_template

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
        nome = request.form.get("nome")
        email = request.form.get("email")
        # logica de verificacao do banco de dados
        cliente_encontrado = cliente_controller.query(request.form.to_dict())
        # redirecionar para tela do sistema
        return "Login realizado com sucesso!" if cliente_encontrado else "404"


@login_cadastro_bp.route("/cadastro", methods=["POST"])
def cadastro():
    if request.method == "POST":
        # pegar dados do formulario
        nome = request.form.get("nome")
        email = request.form.get("email")
        # logica para cadastro do banco de dados
        novo_registro = cliente_controller.create(request.form.to_dict())
        print(request.form.to_dict())
        # redirecionar para tela de login (talvez adicionar notificação)
        return render_template("login.html", nome=nome, email=email)
