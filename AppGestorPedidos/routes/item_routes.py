from flask import Blueprint, jsonify, request
from ..controllers.item_controller import ItemController


# criar blueprint para usar na rota de pedidos
itens_bp = Blueprint('itens', __name__)
# criar controler para pedidos
item_controller = ItemController()


@itens_bp.route('/itens', methods=['GET'])
def get_all_orders():
    orders = item_controller.get_all()
    return jsonify([order.to_dict() for order in orders])


@itens_bp.route('/itens', methods=['POST'])
def create_order():
    data = request.get_json()
    item = item_controller.create(data)
    return jsonify(item.to_dict()), 201