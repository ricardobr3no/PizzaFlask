from flask import Blueprint, jsonify, request

from ..controllers.pedido_controller import PedidoController

# criar blueprint para usar na rota de pedidos
pedidos_bp = Blueprint("pedidos", __name__)
# criar controler para pedidos
pedido_controller = PedidoController()


@pedidos_bp.route("/pedidos", methods=["GET"])
def get_all_pedidos():
    pedidos = pedido_controller.get_all()
    return jsonify([pedido.to_dict() for pedido in pedidos])


@pedidos_bp.route("/pedidos/<int:pedido_id>", methods=["GET"])
def get_pedido(pedido_id: int):
    pedido = pedido_controller.get_by_id(pedido_id)
    return jsonify(pedido.to_dict())


@pedidos_bp.route("/pedidos", methods=["POST"])
def create_pedido():
    data = request.get_json()
    pedido = pedido_controller.create(data)
    return jsonify(pedido.to_dict()), 201


@pedidos_bp.route("/pedidos/<int:pedido_id>", methods=["PUT"])
def update_pedido(pedido_id: int):
    data = request.get_json()
    pedido = pedido_controller.adicionar_item(data, pedido_id)
    return jsonify(pedido), 201


@pedidos_bp.route("/pedidos/<int:pedido_id>", methods=["DELETE"])
def delete_pedido(pedido_id: int):
    deleted = pedido_controller.delete(pedido_id)
    if deleted:
        return jsonify({"message": "Pedido deletado com sucesso!"}), 200
    return jsonify({"message": "Pedido não encontrado"}), 404
