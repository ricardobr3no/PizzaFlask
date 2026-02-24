from .base_controller import BaseController
from ..models import ItemCliente


class PedidoController(BaseController):
    def __init__(self):
        super().__init__(model=ItemCliente)
        