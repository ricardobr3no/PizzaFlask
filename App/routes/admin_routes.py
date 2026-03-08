from flask import Blueprint, render_template, request, redirect, url_for
from ..controllers.item_controller import ItemController
from ..controllers.pedido_controller import PedidoController

# Definimos o prefixo "/admin" para todas as rotas deste arquivo
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# Instanciamos os controllers
item_ctrl = ItemController()
pedido_ctrl = PedidoController()


@admin_bp.route("/", methods=["GET"])
def dashboard():
    # Aqui, no futuro, você pode colocar uma verificação para saber se
    # o usuário logado na session tem o papel de "ADMIN".

    # Busca todos os itens do cardápio
    itens_db = item_ctrl.get_all()

    # Busca todos os pedidos (para o histórico)
    pedidos_db = pedido_ctrl.get_all()

    return render_template("admin.html", itens=itens_db, pedidos=pedidos_db)


@admin_bp.route("/item/adicionar", methods=["POST"])
def adicionar_item():
    # Coleta os dados do formulário HTML
    data = {
        "nome": request.form.get("nome"),
        "preco": float(
            request.form.get("preco").replace(",", ".")
        ),  # Trata a vírgula do decimal
        "descricao": request.form.get("descricao"),
        "imagem": request.form.get(
            "imagem"
        ),  # Para simplificar, estamos usando URL de imagem em texto
    }
    item_ctrl.create(data)
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/item/editar/<int:item_id>", methods=["POST"])
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
def remover_item(item_id):
    # ATENÇÃO: Se um item já estiver num pedido passado, apagar ele pode gerar
    # erro de restrição de chave estrangeira. Uma prática comum em sistemas reais
    # é criar um campo "ativo" (booleano) no banco e apenas desativar o item.
    # Mas para o escopo atual, vamos usar o delete real:
    item_ctrl.delete(item_id)
    return redirect(url_for("admin.dashboard"))
