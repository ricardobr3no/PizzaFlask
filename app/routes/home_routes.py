from datetime import datetime

from flask import (
    request,
    render_template,
    Blueprint,
    session,
    redirect,
    url_for,
    flash,
    send_from_directory,
)
from flask_login import login_required, current_user

from ..utils import HandleFile
from ..models import db
from ..models.pedido import Status

# Importando os seus Controllers!
from ..controllers import (
    UserController,
    ItemController,
    PedidoController,
    ItemPedidoController,
)

home_bp = Blueprint("home", __name__)

# Instanciando os controllers
cliente_ctrl = UserController()
item_ctrl = ItemController()
pedido_ctrl = PedidoController()
item_pedido_ctrl = ItemPedidoController()


@home_bp.route("/home", methods=["GET"])
@login_required
def home():
    # Busca todos os produtos do banco através do Controller
    itens_db = item_ctrl.get_all()
    # Busca o carrinho usando a sua função query() do BaseController
    carrinho = pedido_ctrl.query(
        {"usuario_id": current_user.id, "status": Status.CARRINHO.value}
    )

    itens_carrinho = carrinho.itens if carrinho else []
    total_carrinho = sum(item_pedido.subtotal for item_pedido in itens_carrinho)
    quantidade_itens = sum(item_pedido.quantidade for item_pedido in itens_carrinho)

    return render_template(
        "home.html",
        itens=itens_db,
        itens_carrinho=itens_carrinho,
        total_carrinho=total_carrinho,
        quantidade_itens=quantidade_itens,
        # Usa o nome direto do objeto autenticado
        nome_usuario=(current_user.nome if current_user else "Usuário"),
    )


@home_bp.route("/adicionar/<int:item_id>", methods=["POST"])
@login_required
def adicionar_carrinho(item_id):
    cliente_id = current_user.id
    item = item_ctrl.get_by_id(item_id)

    # Busca o carrinho atual ou cria um novo usando seus Controllers
    carrinho = pedido_ctrl.query(
        {"usuario_id": cliente_id, "status": Status.CARRINHO.value}
    )
    if not carrinho:
        carrinho = pedido_ctrl.create(
            {"usuario_id": cliente_id, "status": Status.CARRINHO.value}
        )

    # Verifica se o lanche já existe no carrinho para somar a quantidade
    item_pedido = item_pedido_ctrl.query({"pedido_id": carrinho.id, "item_id": item.id})
    if item_pedido:
        item_pedido.quantidade += 1
        item_pedido.subtotal = item_pedido.quantidade * item.preco
        db.session.commit()
    else:
        # Cria um novo item no pedido calculando o subtotal
        novo_item = item_pedido_ctrl.create(
            {
                "pedido_id": carrinho.id,
                "item_id": item.id,
                "quantidade": 1,
                "subtotal": item.preco,
            }
        )
        db.session.add(novo_item)
        db.session.commit()

    flash(f"{item.nome} adicionado ao carrinho!", "success")
    return redirect(url_for("home.home"))


@home_bp.route("/remover/<int:item_pedido_id>", methods=["POST"])
@login_required
def remover_carrinho(item_pedido_id: int):
    item_pedido = item_pedido_ctrl.get_by_id(item_pedido_id)
    # Segurança: garante que o usuário só pode apagar itens do próprio pedido
    if item_pedido.pedido.usuario_id == current_user.id:
        db.session.delete(item_pedido)
        db.session.commit()

    return redirect(url_for("home.home"))


@home_bp.route("/finalizar_pedido", methods=["POST"])
@login_required
def finalizar_pedido():
    carrinho = pedido_ctrl.query(
        {"usuario_id": current_user.id, "status": Status.CARRINHO.value}
    )

    # Se tem carrinho e não está vazio, finaliza o pedido usando o Controller
    if carrinho and carrinho.itens:
        pedido_ctrl.update(
            carrinho.id,
            {"status": Status.DISPONIVEL.value, "data": datetime.now()},
        )
        # Notificacao de sucesso
        flash("Pedido finalizado com sucesso! Em breve estará pronto.", "success")
    else:
        # Notificacao de erro (não executa)
        flash("Seu carrinho está vazio. Adicione um lanche primeiro!", "warning")

    return redirect(url_for("home.home"))


@home_bp.route("/item/imagem/<filename>")
def exibir_imagem(filename: str):
    print(filename)
    # Esta função busca o arquivo na pasta 'uploads' e o envia para o navegador
    return send_from_directory(
        HandleFile.UPLOAD_FOLDER,
        filename,
        as_attachment=False,  # Define se abre no navegador ou baixa
    )
