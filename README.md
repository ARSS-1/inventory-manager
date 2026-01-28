# Inventory Manager API 🚀
v 0.1.0

[Português]
Esta é uma API RESTful desenvolvida em Python para o gerenciamento de produtos com autenticação de usuários. O sistema garante que cada produto seja vinculado ao seu criador, aplicando regras de negócio para proteger os dados. Cada inventário é independente, e cada produto só pode ser cadastrado uma vez.

[English]
This is a RESTful API developed in Python for product management with user authentication. The system ensures each product is linked to its creator, applying business rules to protect data. Each inventory is independent, and each product can be added only once.

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
| POST | `/users/register` | Novo usuário / New user | No |
| POST | `/users/login` | Login / Authentication | No |
| GET | `/users/profile` | Perfil do usuário / User Profile | **Yes** |
| POST | `/products` | Criar produto / Create product | **Yes** |
| PATCH | `/products/<id>`| Editar produto / Update product | **Yes (Owner)** |
| DELETE| `/products/<id>`| Deletar produto / Delete product | **Yes (Owner)** |
