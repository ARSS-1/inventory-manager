# Inventory Manager API 🚀
v 0.1.2

### 🇧🇷 Português
Esta é uma API RESTful desenvolvida em Python para o gerenciamento de produtos com autenticação de usuários. O sistema garante que cada produto seja vinculado ao seu criador, aplicando regras de negócio para proteger os dados. Cada inventário é independente, e cada produto só pode ser cadastrado uma vez para cada usuário. Senhas são salvas em hash, tornando o banco de dados mais seguro.

### 🇺🇸 English
This is a RESTful API developed in Python for product management with user authentication. The system ensures each product is linked to its creator, applying business rules to protect data. Each inventory is independent, and each product can be added only once for each user. Passwords are stored in hash, making the database safer.

---

## 🛠️ Tecnologias / Technologies

- **Python 3**
- **Flask**: Micro-framework web.
- **SQLAlchemy**: ORM para banco de dados / Database ORM.
- **Pydantic V2**: Validação e schemas / Validation and schemas (`BeforeValidator`, `model_config`).
- **Flask-JWT-Extended**: Autenticação / Authentication (JWT).

---

## 🌟 Destaques Técnicos / Technical Highlights

### 🇧🇷 Português
- **Relacionamento 1:N**: Usuários possuem múltiplos produtos.
- **Segurança de Registro**: Apenas o dono pode editar ou excluir seus próprios produtos (403 Forbidden).
- **Transformação de Dados**: Uso de validadores customizados para retornar apenas nomes de produtos no perfil.

### 🇺🇸 English
- **1:N Relationship**: Users can have multiple products.
- **Resource Protection**: Only the owner can edit or delete their own products (403 Forbidden).
- **Data Transformation**: Used custom validators to return a clean list of product names in the user profile.

---

## 🛤️ Endpoints

| Método/Method | Rota/Route | Descrição/Description | Protegida/Protected |
| :--- | :--- | :--- | :--- |
| POST | `/users/new` | Novo usuário / New user | No |
| POST | `/users/login` | Login / Authentication | No |
| GET | `/users/profile` | Perfil do usuário / User Profile | **Yes** |
| POST | `/products/new` | Criar produto / Create product | **Yes** |
| GET | `/products` | Lista todos os produtos do usuário/ List all user's products | **Yes** |
| PATCH | `/products/<id>`| Editar produto / Update product | **Yes (Owner)** |
| DELETE| `/products/<id>`| Deletar produto / Delete product | **Yes (Owner)** |

* A rota [GET] '/products' aceita os parâmetros de busca nome (name), preço (price) e página (page)
* Para rotas protegidas, use o Bearer Token no header the autorização.


* The [GET] '/products' route allows the query parameters name, price and page.
* For protected routes, use the Bearer Token in the Authorization header

## Como Usar / How to Use:

### 🇧🇷 Português
- Você deve ter o Poetry e o Python (>3.10) instalados;
- Navegue até a pasta raiz do projeto pelo terminal;
- Rode o comando "poetry install" para instalar todas as dependênicias;
- Rode o comando "flask --app app.main run" para iniciar o servidor.

### 🇺🇸 English
- You must have Poetry and Python (>3.10) installed;
- Navigate to the root folder on your terminal;
- Run "poetry install"
- Run "flask --app app.main run" to start the server.

## Exemplos / Examples:

### /users/new:
{
    'username': 'Usuario',
    'password': 'senha8dig' 
}

return {'message':'Usuário criado com sucesso!'}

### /products/new:
{
    'name': 'nome do produto',
    'price': 10.00,
    'description' : 'descrição opcional'
    'quantity': 1
}

return {'message':'Produto criado com sucesso!'}