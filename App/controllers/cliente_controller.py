from .base_controller import BaseController
from ..models.cliente import Cliente
from flask_login import UserMixin


class ClienteController(BaseController, UserMixin):
    def __init__(self):
        super().__init__(model=Cliente)
