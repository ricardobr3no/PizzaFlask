from .base_controller import BaseController
from ..models.cliente import Cliente


class ClienteController(BaseController):
    def __init__(self):
        super().__init__(model=Cliente)
