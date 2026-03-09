from flask import request, render_template, Blueprint, session, redirect, url_for, flash
from datetime import datetime

from ..models import db
from ..models.pedido import Status
from ..models.item_pedido import ItemPedido

# Importando os seus Controllers!
from ..controllers.cliente_controller import ClienteController
from ..controllers.item_controller import ItemController
from ..controllers.pedido_controller import PedidoController

home_bp = Blueprint("home", __name__)

# Instanciando os controllers
cliente_ctrl = ClienteController()
item_ctrl = ItemController()
pedido_ctrl = PedidoController()


@home_bp.route("/home", methods=["GET"])
def home():
    # 1. AUTENTICAÇÃO: Verifica se o usuário está logado
    if "cliente_id" not in session:
        # Mock de login para o usuário de ID 1 (pode remover quando tiver a tela de login pronta)
        session["cliente_id"] = 1

    cliente_id = session["cliente_id"]

    # Usa o controller para buscar o cliente
    cliente = cliente_ctrl.get_by_id(cliente_id)
    # 2. Busca todos os produtos do banco através do Controller
    itens_db = item_ctrl.get_all()
    # 3. Busca o carrinho usando a sua função query() do BaseController
    carrinho = pedido_ctrl.query(
        {"cliente_id": cliente_id, "status": Status.CARRINHO.value}
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
        nome_usuario=cliente.nome if cliente else "Usuário",
    )


@home_bp.route("/adicionar/<int:item_id>", methods=["POST"])
def adicionar_carrinho(item_id):
    if "cliente_id" not in session:
        return redirect(url_for("home.home"))

    cliente_id = session["cliente_id"]
    item = item_ctrl.get_by_id(item_id)

    # Busca o carrinho atual ou cria um novo usando seus Controllers
    carrinho = pedido_ctrl.query(
        {"cliente_id": cliente_id, "status": Status.CARRINHO.value}
    )
    if not carrinho:
        carrinho = pedido_ctrl.create(
            {"cliente_id": cliente_id, "status": Status.CARRINHO.value}
        )

    # Verifica se o lanche já existe no carrinho para somar a quantidade
    item_pedido = ItemPedido.query.filter_by(
        pedido_id=carrinho.id, item_id=item.id
    ).first()

    if item_pedido:
        item_pedido.quantidade += 1
        item_pedido.subtotal = item_pedido.quantidade * item.preco
        db.session.commit()
    else:
        # Cria um novo item no pedido calculando o subtotal
        novo_item = ItemPedido(
            pedido_id=carrinho.id,
            item_id=item.id,
            quantidade=1,
            subtotal=item.preco,
        )
        db.session.add(novo_item)
        db.session.commit()

    flash(f"{item.nome} adicionado ao carrinho!", "success")
    return redirect(url_for("home.home"))


@home_bp.route("/remover/<int:item_pedido_id>", methods=["POST"])
def remover_carrinho(item_pedido_id):
    if "cliente_id" not in session:
        return redirect(url_for("home.home"))

    item_pedido = ItemPedido.query.get_or_404(item_pedido_id)

    # Segurança: garante que o usuário só pode apagar itens do próprio pedido
    if item_pedido.pedido.cliente_id == session["cliente_id"]:
        db.session.delete(item_pedido)
        db.session.commit()

    return redirect(url_for("home.home"))


@home_bp.route("/finalizar_pedido", methods=["POST"])
def finalizar_pedido():
    if "cliente_id" not in session:
        return redirect(url_for("home.home"))

    cliente_id = session["cliente_id"]
    carrinho = pedido_ctrl.query(
        {"cliente_id": cliente_id, "status": Status.CARRINHO.value}
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
