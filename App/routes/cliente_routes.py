from flask import Blueprint, jsonify, request

from ..controllers.cliente_controller import ClienteController

# criamos blueprint para clientes
clientes_bp = Blueprint("clientes", __name__)
# Instancia o controller genérico para Client
client_controller = ClienteController()


# criamos rotas para clientes
@clientes_bp.route("/clientes", methods=["GET"])
def get_clients():
    clients = client_controller.get_all()
    print(clients)
    return jsonify([client.to_dict() for client in clients]), 200


@clientes_bp.route("/clientes", methods=["POST"])
def create_client():
    data = request.get_json()
    # O controller lida com a criação e já salva no banco
    novo_cliente = client_controller.create(data)
    return jsonify(
        {"message": "Client created successfully", "cliente": novo_cliente.to_dict()}
    ), 201


@clientes_bp.route("/clientes/<int:id>", methods=["PUT"])
def update_cliente_by_id(id: int, data: dict):
    cliente_atualizado = client_controller.update(id, data)
    return cliente_atualizado, 201


@clientes_bp.route("/clientes/<int:id>", methods=["DELETE"])
def delete_cliente_by_id(id: int):
    deleted = client_controller.delete(id)
    if deleted:
        return jsonify({"message": "Cliente deletado com sucesso!"}), 200
    return jsonify({"message": "Client not found"}), 404
