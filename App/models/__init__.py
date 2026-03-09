from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .cliente import Cliente
from .item import Item
from .item_pedido import ItemPedido
from .pedido import Pedido
