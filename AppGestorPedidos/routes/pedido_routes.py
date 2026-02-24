from flask import Blueprint, jsonify, request
from ..controllers.pedido_controller import PedidoController


# criar blueprint para usar na rota de pedidos
pedidos_bp = Blueprint('pedidos', __name__)
# criar controler para pedidos
pedido_controller = PedidoController()


@pedidos_bp.route('/pedidos', methods=['GET'])
def get_all_pedidos():
    pedidos = pedido_controller.get_all()
    return jsonify([pedido.to_dict() for pedido in pedidos])


@pedidos_bp.route('/pedidos', methods=['POST'])
def create_pedido():
    data = request.get_json()
    pedido = pedido_controller.create(data)
    return jsonify(pedido.to_dict()), 201
