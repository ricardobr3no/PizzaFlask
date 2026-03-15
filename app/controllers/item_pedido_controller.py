from .base_controller import BaseController
from ..models import ItemPedido


class ItemPedidoController(BaseController):
    def __init__(self):
        super().__init__(model=ItemPedido)
