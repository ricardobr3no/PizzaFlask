from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .usuario import Usuario
from .item import Item
from .item_pedido import ItemPedido
from .pedido import Pedido
