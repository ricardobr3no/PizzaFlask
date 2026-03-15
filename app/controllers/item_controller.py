from .base_controller import BaseController
from ..models.item import Item


class ItemController(BaseController):
    def __init__(self):
        super().__init__(model=Item)
