from .base_controller import BaseController
from ..models.pedido import Pedido
from ..models.item_pedido import ItemPedido
from ..models.item import Item


class PedidoController(BaseController):
    def __init__(self):
        super().__init__(model=Pedido)

    def adicionar_item(self, data: dict, pedido_id: int):
        """
        'data' deve conter: {"item_id": 1, "quantidade": 2}
        """
        # 1. Verificar se o item existe
        item = Item.query.get(data.get("item_id"))
        if not item:
            return {"erro": "Item não encontrado"}, 404

        # 2. Verificar se o pedido existe
        pedido = Pedido.query.get(pedido_id)
        if not pedido:
            return {"erro": "Pedido não encontrado"}, 404

        try:
            # 3. Criar a relação Item-Pedido
            novo_item_pedido = ItemPedido(
                pedido_id=pedido_id,
                item_id=item.id,
                quantidade=data.get("quantidade", 1),  # Padrão 1 se não enviado
            )

            self.db.session.add(novo_item_pedido)
            self.db.session.commit()

            return {
                "mensagem": "Item adicionado com sucesso!",
                "item": item.nome,
                "subtotal": item.preco * novo_item_pedido.quantidade,
            }, 201

        except Exception as e:
            self.db.session.rollback()
            return {"erro": f"Erro ao salvar: {str(e)}"}, 500
