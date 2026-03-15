"""
script para popular inicialmente o banco de dados
"""

import logging


from app import App
from app.controllers import UserController, ItemController
from app.models import db
from werkzeug.security import generate_password_hash, check_password_hash

dados_admin = {"nome": "admin", "email": "admin@email.com", "senha": "123456"}
dados_admin["senha"] = generate_password_hash(dados_admin["senha"])

dados_itens = [
    {
        "nome": "X-Burguer Clássico",
        "preco": 25.90,
        "imagem": "xbuerger.jpg",
        "descricao": "Pão brioche, blend bovino 150g, queijo cheddar derretido e maionese artesanal.",
    },
    {
        "nome": "Batata Frita Rústica",
        "preco": 18.00,
        "imagem": "batata.jpg",
        "descricao": "Porção de 300g de batatas cortadas à mão, temperadas com alecrim e páprica.",
    },
    {
        "nome": "Cheddar Bacon Monster",
        "preco": 34.50,
        "imagem": "cheddar_bacon.jpg",
        "descricao": "Dois blends de 150g, muito bacon crocante, cebola caramelizada e dose dupla de cheddar.",
    },
    {
        "nome": "Suco de Laranja Natural",
        "preco": 10.00,
        "imagem": "suco_laranja.jpg",
        "descricao": "Suco natural da fruta, 400ml, sem adição de conservantes.",
    },
    {
        "nome": "Milkshake de Nutella",
        "preco": 22.00,
        "imagem": "shake_nutella.jpg",
        "descricao": "Sorvete de baunilha batido com Nutella autêntica e chantilly.",
    },
]


app = App(force=True)
user_ctrl = UserController()
item_ctrl = ItemController()

with app.app.app_context():
    # criar o perfil do admin
    user_ctrl.create(dados_admin)

    for dados_item in dados_itens:
        item_ctrl.create(dados_item)
