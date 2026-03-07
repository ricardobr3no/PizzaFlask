from flask import Blueprint, jsonify, request

from App.routes.pedido_routes import pedido_controller

from ..controllers.item_controller import ItemController

# criar blueprint para usar na rota de pedidos
itens_bp = Blueprint("itens", __name__)
# criar controler para pedidos
item_controller = ItemController()


@itens_bp.route("/itens", methods=["GET"])
def get_all_orders():
    orders = item_controller.get_all()
    return jsonify([order.to_dict() for order in orders])


@itens_bp.route("/itens/<int:id>", methods=["GET"])
def get_by_id(id: int):
    pedido = pedido_controller.get_by_id(id)
    if pedido:
        return jsonify(pedido.to_dict()), 200
    return jsonify({"message": "pedido nao encontrado"}), 404


@itens_bp.route("/itens", methods=["POST"])
def create_order():
    data = request.get_json()
    item = item_controller.create(data)
    return jsonify(item.to_dict()), 201


@itens_bp.route("/itens/<int:id>", methods=["PUT"])
def update_order(id: int, data: dict):
    order = item_controller.update(id, data)
    return order, 201


@itens_bp.route("/itens/<int:id>", methods=["DELETE"])
def delete_order(id: int):
    deleted = item_controller.delete(id)
    if deleted:
        return jsonify({"message": "Order deleted successfully"}), 200
    return jsonify({"message": "Order not found"}), 404
