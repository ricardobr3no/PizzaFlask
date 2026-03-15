# BurguerTech

O **BurguerTech** é uma aplicação web desenvolvida em Flask para simplificar o fluxo de pedidos de uma lanchonete. Com ele, é possível cadastrar produtos, gerenciar o carrinho de compras e acompanhar o status da produção.

---

## 🚀 Funcionalidades

* **Cardápio Digital:** Visualização de produtos com categorias (lanches, bebidas, sobremesas).
* **Gestão de Pedidos:** Criação de pedidos com múltiplos itens.
* **Controle de Estoque:** Cadastro e edição de produtos (Preço, Descrição, Disponibilidade).
* **Status em Tempo Real:** Acompanhamento do pedido (Recebido -> Em Preparo -> Pronto -> Entregue).

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3.x + Flask
* **Banco de Dados:** SQLite (ou PostgreSQL/MySQL)
* **Frontend:** HTML5, CSS3 (Bootstrap 5), Jinja2
* **ORM:** Flask-SQLAlchemy

---

## 📦 Como Instalar e Rodar

Siga os passos abaixo para configurar o ambiente local:

1. **Clone o repositório:**
```bash
git clone https://github.com/ricardobr3no/PizzaFlask.git
cd PizzaFlask

```


2. **Crie um ambiente virtual:**
```bash
python -m venv venv

```


3. **Ative o ambiente virtual:**
* Windows: `venv\Scripts\activate`
* Linux/macOS: `source venv/bin/activate`


4. **Instale as dependências:**
```bash
pip install -r requirements.txt

```


5. **Execute a aplicação:**
```bash
python run.py

```
Acesse: `http://127.0.0.1:5000/login`

----
### 🔐 Acesso e Permissões
O sistema possui um controle de níveis de acesso (RBAC) simplificado:
  - Clientes: Novos usuários registrados pelo formulário de cadastro recebem automaticamente o perfil cliente. Eles podem visualizar o cardápio e realizar pedidos. 
  - Administrador: Possui acesso total ao painel de gerenciamento, cadastro de produtos e alteração de status de pedidos.

Credenciais de Teste (Admin)

Para fins de homologação e testes das funcionalidades administrativas, utilize os dados abaixo:

    📧 E-mail: admin@email.com

    🔑 Senha: 123456

🛠️ Como rodar o Setup Inicial

Popular o Banco de Dados (Opcional):

  ```bash 
  python seed.py
  ```
---

## 🗺️ Estrutura do Banco de Dados

O sistema utiliza três entidades principais para garantir a integridade dos dados:

* **Usuario:** Nome, email, senha.
* **Item:** Nome, preco, descricao, imagem.
* **Pedido:** Dados do cliente, data/hora, status, itens.
* **ItemPedido:** Tabela intermediária que vincula produtos a pedidos com suas respectivas quantidades.

---

## 🛣️ Roadmap / Próximos Passos

* [x] Implementar autenticação para funcionários (Login/Logout).
* [ ] Adicionar Painel da Cozinha para visualização de pedidos pendentes para a equipe de produção.
* [ ] Gerar relatórios de vendas em PDF.
* [ ] Integrar com API de pagamentos.
* [ ] Adicionar suporte a notificações via WhatsApp.

