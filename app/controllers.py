from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from sqlalchemy import select, inspect
from sqlalchemy.exc import IntegrityError
from app.database import db
from app.models import Product, User
from app.schemas import ProductIn, ProductOut, ProductUpdate, UserIn, UserOut
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

product_bp = Blueprint("products", __name__)
user_bp = Blueprint("users", __name__)


# ADD A NEW PRODUCT
@product_bp.route("/products/new", methods=["POST"])
@jwt_required()
def new_product():
    try:
        # SOLICITA OS DADOS
        data = request.get_json()

        # VALIDA USANDO O SCHEMA
        validated = ProductIn(**data)

        # INSTANCIA  O MODELO PRODUCT, PASSANDO VALIDATED COMO KWARGS
        # A FUNÇÃO MODEL_DUMP() TRANSFORMA O OBJ DE VALIDAÇÃO EM DICIONÁRIO
        new_product = Product(**validated.model_dump())
        new_product.user_id = int(get_jwt_identity())

        # ADICIONA À SESSÃO DO DB E COMITA
        db.session.add(new_product)
        db.session.commit()

        return {"message": "Produto criado com sucesso!"}, 201

    # TRATATIVAS DE ERRO
    except ValidationError as e:
        return jsonify(e.errors()), 400

    except IntegrityError:
        db.session.rollback()
        return {"message": "O produto já existe."}, 400


# LISTA TODOS OS PRODUTOS; FILTRA POR NOME OU PRECO
@product_bp.route("/products", methods=["GET"])
@jwt_required()
def list_products():
    query = select(Product).where(Product.user_id == int(get_jwt_identity()))
    name_filter = request.args.get("name")
    max_price_filter = request.args.get("price")

    # ORGANIZA OS RESULTADOS EM N PAGES
    page = request.args.get("page", 1)  # PAGINA ATUAL, SOLICITADO AO USUÁRIO
    per_page = request.args.get(
        "per_page", 2
    )  # ITEMS POR PÁGINA, SOLICITADO AO USUÁRIO

    try:
        page = int(page)
        per_page = int(per_page)
    except ValueError:
        return {
            "message": "O número de páginas e de items por páginas devem ser números inteiros."
        }

    # DETERMINA O OFFSET - QUANTOS ITEMS ELE DEVE PULAR AO PASSAR DE PÁGINA
    offset_value = (page - 1) * per_page

    # FILTRO POR NOME. ACEITA PARCIAL.
    if name_filter:
        query = query.where(Product.name.ilike(f"%{name_filter}%"))

    # FILTRO POR PREÇO MÁXIMO.
    if max_price_filter:
        try:
            max_price_filter = float(max_price_filter)
            query = query.where(Product.price <= max_price_filter)

        # TRATATIVAS DE ERRO
        except ValueError:
            return {"message": "Valor inválido. Digite um número inteiro."}, 400

    # ORGANIZA O RESULTADO; ATIVA O LIMITE POR PÁGINA E O OFFSET
    query = (
        query.order_by(Product.price.asc()).limit(per_page).offset(offset_value)
    )  # ORDER BY PRICE

    # O RESULTADO DA BUSCA É UMA TUPLA, COMO CADA UM DOS PRODUTOS RESULTADO
    # O SCALARS/ALL GARANTE QUE SEJAM UTILIZADOS CADA UM DOS VALORES DENTRO DA TUPLA
    results = db.session.scalars(query).all()

    # DEFINE O RETORNO DOS RESULTADOS USANDO O SCHEMA USEROUT
    output = [ProductOut.model_validate(result).model_dump() for result in results]

    return (
        jsonify(
            {"items": output, "page": page, "per_page": per_page, "total": len(output)}
        ),
        200,
    )


# PROCURA UM PRODUTO PELO ID, E O DELETA.
@product_bp.route("/products/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_product(id):
    query = select(Product).where(Product.id == id)
    user_id = int(get_jwt_identity())

    product = db.session.scalar(query)

    if not product:
        return {"message": "Produto não encontrado!"}, 404

    if product.user_id != user_id:
        return {"message": "Usuário não autorizado."}, 403

    db.session.delete(product)
    db.session.commit()

    return {"message": "Produto removido com sucesso."}, 200


# PROCURA UM PRODUTO PELO ID, E O EXIBE.
@product_bp.route("/products/<int:id>", methods=["GET"])
@jwt_required()
def list_product_by_id(id):
    query = select(Product).where(Product.id == id)
    user_id = int(get_jwt_identity())

    product = db.session.scalar(query)

    if not product:
        return {"message": "Produto não encontrado!"}, 404

    if product.user_id != user_id:
        return {"message": "Usuário não autorizado."}, 403

    output = ProductOut.model_validate(product).model_dump()

    return output, 201


# PROCURA UM PRODUTO PELO ID, E O ATUALIZA
@product_bp.route("/products/<int:id>", methods=["PATCH", "PUT"])
@jwt_required()
def update_product(id):

    query = select(Product).where(Product.id == id)
    user_id = int(get_jwt_identity())

    product = db.session.scalar(query)

    if not product:
        return {"message": "Produto não encontrado!"}, 404

    if user_id != product.user_id:
        return {"message": "Usuário não autorizado!"}, 403

    try:
        data = request.get_json()
        validated = ProductUpdate(**data)

        # O EXCLUDE_UNSET GARANTE QUE SÓ SEJAM REGISTRADOS OS VALORES PASSADOS
        # VALORES NONE SERÃO IGNORADOS
        update_data = validated.model_dump(exclude_unset=True)

        # PARA CADA CHAVE, VALOR NO DICIONÁRIO UPDATE_DATA
        # SET NO PRODUTO (RESULTADO DA BUSCA), PARA A COLUNA KEY, O VALOR VALUE
        for key, value in update_data.items():
            setattr(product, key, value)

        db.session.commit()

        return {"message": "Produto atualizado com sucesso!"}, 200

    # TRATAIVA DE ERRO
    except ValidationError as e:
        return jsonify(e.errors()), 400


@user_bp.route("/users/new", methods=["POST"])
def new_user():
    try:
        data = request.get_json()
        validate = UserIn(**data)

        password_hash = generate_password_hash(validate.password)

        new_user = User(username=validate.username, password_hash=password_hash)

        db.session.add(new_user)
        db.session.commit()

        return {"message": "Usuário criado com sucesso!"}, 201

    except ValidationError as e:
        return jsonify(e.errors()), 400

    except IntegrityError:
        return {"message": "Usuário já cadastrado."}


@user_bp.route("/users/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        data_validated = UserIn(**data)

        query = select(User).where(User.username == data_validated.username)
        user = db.session.execute(query).scalar()

        if user:
            if check_password_hash(user.password_hash, data_validated.password):
                access_token = create_access_token(identity=str(user.id))
                return {
                    "message": "login efetuado com sucesso",
                    "access_token": access_token,
                }, 200

        return {"message": "Usuário ou senha inválidos"}, 401

    except ValidationError as e:
        return jsonify(e.errors(), 400)


@user_bp.route("/users/profile", methods=["GET"])
@jwt_required()
def show_profile():
    current_user_id = get_jwt_identity()

    current_user = db.session.get(User, current_user_id)

    output = UserOut.model_validate(current_user).model_dump()

    return jsonify(output)
