import os
from functools import wraps
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_from_directory,
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from . import HandleFile
from ..controllers import ItemController, PedidoController

# Definimos o prefixo "/admin" para todas as rotas deste arquivo
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# Instanciamos os controllers
item_ctrl = ItemController()
pedido_ctrl = PedidoController()


# decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 1. Verifica se o usuário está logado
        if not current_user.is_authenticated:
            flash("Você precisa estar logado para acessar esta página.", "warning")
            return redirect(url_for("login_cadastro.login"))

        # 2. Verifica se a role (papel) dele é ADMIN
        # Lembrando que no seu model configuramos role = "ADMIN" ou Role.ADMIN.value
        if current_user.role != "ADMIN":
            # Retorna erro 403 (Proibido) ou redireciona
            flash("Acesso negado. Área restrita para administradores.", "danger")
            return redirect(
                url_for("home.home")
            )  # Mude 'home' para o nome da sua rota principal

        return f(*args, **kwargs)

    return decorated_function


@admin_bp.route("/", methods=["GET"])
@admin_required
def dashboard():
    # Aqui, no futuro, você pode colocar uma verificação para saber se
    # o usuário logado na session tem o papel de "ADMIN".

    # Busca todos os itens do cardápio
    itens_db = item_ctrl.get_all()
    # Busca todos os pedidos (para o histórico)
    pedidos_db = pedido_ctrl.get_all()

    return render_template("admin.html", itens=itens_db, pedidos=pedidos_db)


@admin_bp.route("/item/adicionar", methods=["POST"])
@admin_required
def adicionar_item():
    # Coleta os dados do formulário HTML
    file_image = request.files["imagem"]
    file_image.filename = file_image.filename.replace(
        file_image.filename, request.form.get("nome") + ".jpg"
    )
    data = {
        "nome": request.form.get("nome"),
        "preco": float(
            request.form.get("preco").replace(",", ".")
        ),  # Trata a vírgula do decimal
        "descricao": request.form.get("descricao"),
        "imagem": HandleFile.get_secure_name(file_image),
    }
    # faz upload do arquivo anexado
    HandleFile.upload_file(file_image)
    # adiciona registro no banco de dados
    item_ctrl.create(data)

    flash("Item cadastrado com sucessop!", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/item/editar/<int:item_id>", methods=["POST"])
@admin_required
def editar_item(item_id):
    data = {
        "nome": request.form.get("nome"),
        "preco": float(request.form.get("preco").replace(",", ".")),
        "descricao": request.form.get("descricao"),
        "imagem": request.form.get("imagem"),
    }
    item_ctrl.update(item_id, data)
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/item/remover/<int:item_id>", methods=["POST"])
@admin_required
def remover_item(item_id):
    # ATENÇÃO: Se um item já estiver num pedido passado, apagar ele pode gerar
    # erro de restrição de chave estrangeira. Uma prática comum em sistemas reais
    # é criar um campo "ativo" (booleano) no banco e apenas desativar o item.
    # Mas para o escopo atual, vamos usar o delete real:
    item_ctrl.delete(item_id)
    return redirect(url_for("admin.dashboard"))
