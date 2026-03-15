from .base_controller import BaseController

from ..models import Usuario

from flask_login import UserMixin


class UserController(BaseController, UserMixin):

    def __init__(self):

        super().__init__(model=Usuario)
